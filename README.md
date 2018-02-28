```
      _ _    _ _             
  ___(_) | _(_) | ___  _ __  
 / __| | |/ / | |/ _ \| '_ \ 
| (__| |   <| | | (_) | |_) |
 \___|_|_|\_\_|_|\___/| .__/ 
                      |_|    
```

Cikilop is a simple and easy to use mongo migration tool that encourages you to write your migration scripts in Python.
All you need is docker (or python 3.6).

### Usage

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

__2. You need to name your script as `01-xxxx.py`, it must start with a number. Cikilop sorts your migration files using that number.__

_Caveat: When applying the migration, scripts run with ascending order (e.g. `01-mig.py`, `02-mig.py`, `03-mig.py`).
 When reverting the migration, scripts run with descending order (e.g. `03-mig.py`, `02-mig.py`, `01-mig.py`)._

__3. Prepare your simple configuration file:__

```json
{
  "db_name" : "deneme",
  "migrations_coll_name" : "migration_list",
  "mongo_uri" : "mongodb://username:pass@127.0.0.1:27017..."
}
```

_Note: The name you set with __migrations_coll_name__ is used by cikilop itself. It creates a collection and stores the migration records in it._

__4. Run it!__

`ciki`

### Important Notes:



Under construction.