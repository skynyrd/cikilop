```
      _ _    _ _             
  ___(_) | _(_) | ___  _ __  
 / __| | |/ / | |/ _ \| '_ \ 
| (__| |   <| | | (_) | |_) |
 \___|_|_|\_\_|_|\___/| .__/ 
                      |_|    
```

Cikilop is a simple and easy to use mongo migration tool that encourages you to write your migration scripts in Python.
All you need is docker.

### Usage

1. Build your migration script with only two functions:

```py
def success(db):
    col = db["denemecol"]
    col.insert_one({"_id": 1})


def fail(db):
    col = db["denemecol"]
    col.remove({"_id": 1})
```
Both functions must have an input parameter `db`, which cikilop ships to you. Indeed, it is regular `pymongo` database object (`pymongo.database.DataBase`).

2. You need to name your script as `01-xxxx.py`, it must start with a number. Cikilop sorts your migration files using that number. 

_When applying the migration, scripts run with ascending order (e.g. `01-mig.py`, `02-mig.py`, `03-mig.py`).
 When reverting the migration, scripts run with descending order (e.g. `03-mig.py`, `02-mig.py`, `01-mig.py`)._


Under construction.