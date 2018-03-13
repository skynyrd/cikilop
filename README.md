[![Build Status](https://travis-ci.org/skynyrd/cikilop.svg?branch=master)](https://travis-ci.org/skynyrd/cikilop)
[![Docker Hub](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/skynyrd/cikilop/)

```
      _ _    _ _             
  ___(_) | _(_) | ___  _ __  
 / __| | |/ / | |/ _ \| '_ \ 
| (__| |   <| | | (_) | |_) |
 \___|_|_|\_\_|_|\___/| .__/ 
                      |_|    
```
Cikilop is a simple and easy to use data migration tool for MongoDB that encourages you to write your migration scripts in Python.
All you need is docker (or python 3.6).

### Why it's the tool you are looking for?
1. You need to manage your migrations commit by commit in your CI pipeline. A commit can have more than one new migration, in that case you need to migrate them in order, and if commit fails, you need to revert them in reverse order.
2. You want simply revert your migration from the CLI
3. Your project is written in Python, you are more comfortable with pymongo then plain mongo script.
4. You don't want to depend anything except docker
5. You just liked it's name <3

### Usage

What you need: Prepare your migration scripts, prepare your config, run cikilop. That's it.

[![asciicast](https://asciinema.org/a/jJnpgClAfmCKASiKW02ZlLLRR.png)](https://asciinema.org/a/jJnpgClAfmCKASiKW02ZlLLRR)

__1. Build your migration script with only two functions:__

```py
def success(db):
    col = db["example_collection"]
    col.insert_one({"_id": 1})


def fail(db):
    col = db["example_collection"]
    col.remove({"_id": 1})
```
Both functions must have an input parameter `db`, which cikilop ships to you. Indeed, it is regular `pymongo` database object (`pymongo.database.DataBase`).

__2. You need to name your script as `01-xxxx.py`, it must start with a number with dash. Cikilop sorts your migration files using that number.__

_Caveat: When applying the migration, scripts run with ascending order (e.g. `01-mig.py`, `02-mig.py`, `03-mig.py`).
 When reverting the migration, scripts run with descending order (e.g. `03-mig.py`, `02-mig.py`, `01-mig.py`)._

__3. Prepare your simple configuration file, Its name must be config.ENVIRONMENT.json (ENVIRONMENT should be same as you used in run command):__

```json
{
  "db_name" : "exampledb",
  "migrations_coll_name" : "migration_list",
  "mongo_uri" : "mongodb://username:pass@127.0.0.1:27017..."
}
```

_Note: The name you set with __migrations_coll_name__ is used by cikilop itself. It creates a collection and stores the migration records in it._

__4. Run it!__

Use the wrapper script (it also uses docker):

1. `curl https://raw.githubusercontent.com/skynyrd/cikilop/master/ciki.sh --output ciki.sh && chmod +x ciki.sh`

2. `sudo ./ciki.sh -e ENVIRONMENT -c ABSOLUTE_CONFIG_FILE_PATH -m ABSOLUTE_MIGRATIONS_FOLDER_PATH`

e.g.: `sudo ./ciki.sh -e local -c $(pwd)/config.local.json -m $(pwd)/migrations`

To revert, add `-r true`

or use docker directly:

```bash
docker run -e env=local -v ABSOLUTE_CONFIG_FILE_PATH:/app/src/config/config.local.json -v ABSOLUTE_MIGRATIONS_FOLDER_PATH:/app/src/migrations skynyrd/cikilop

e.g. docker run -e env=local -v $(pwd)/config.local.json:/app/src/config/config.local.json -v $(pwd)/migrations:/app/src/migrations skynyrd/cikilop
```

To revert, add `--revert` to `docker run` command

### Behind the scenes:

* When migrating:
    * Cikilop first checks your files in your migrations folder with its migration collection in your mongo.
    * If your folder has any new files, or any files that is already reverted in mongo, cikilop runs success functions of that files. (ordering: first 01-example.py, then 02-example.py)
* When reverting:
    * Cikilop gets last created migration from its migration collection. It may have more than one files.
    * It checks the files in last created migration with the files in your migrations folder.
    * Takes their union.
    * Reverts them by calling fail functions of the files. (ordering: first 02-example.py then 01-example.py)

Thanks!

### License

* GNU GPL v3
