# Database Management

This section describes how to manage the database, including seeding it with initial data and dropping collections. The
operations are handled using the `db.py` and `__main__.py` files.

## Database Operations

### Drop Collections

To drop all collections from the database, use the `drop()` function. This operation will remove all documents from the
specified collections.

**Function:** `drop()`

**Usage:**

```python
from src.database.db import drop

drop()
```

**Collections Dropped:**

`blog`
`links`
`experiences`
`contact`
`projects`
`newsletter`
`subscriber`
`comments`
`book`
`technology`

Note: The `drop_user()` function specifically drops the user collection.

Function: `drop_user()`

**Usage:**

```python
from src.database.db import drop_user

drop_user()
```

### Seed Collections

To seed the database with initial data, use the `seed()` function. This operation will insert predefined data into the
specified collections.

Function: `seed()`

**Usage:**

```python
from src.database.db import seed

seed()
```

**Data Seeded:**

`blog`
`links`
`experiences`
`contact`
`projects`
`newsletter`
`subscriber`
`comments`
`book`
`technology`

**Note**: The `seed_user()` function specifically seeds the user collection.

**Function**: `seed_user()`

**Usage:**

```python
from src.database.db import seed_user

seed_user()
```

### Running Database Management Operations

The `__main__.py` file provides a command-line interface for running the database management operations. When executed, it will prompt you to perform the following actions:

1. Drop and Seed All Collections:
   - Type `y` to drop all collections and seed them with initial data.

2. Drop and Seed User Collection:
   - Type `y` to drop the user collection and seed it with user data.
   
3. Write Document Fields to output.txt:
   - Type `y` to write the fields of all collections to output.txt.

**Usage:**

```shell
python -m src.main
```

**Prompts:**

1. Drop and Seed:
   - `Type "y" if you want to run drop and seed:`
2. Drop User:
   - `If you want to drop user type "y":`
3. Write Document Fields:
   - `Type "y" if you want to write the document and press enter:`

**Example:**
```text
Type "y" if you want to run drop and seed: y
drop() and seed() initialized
# Collections are dropped and seeded

If you want to drop user type "y": y
# User collection is dropped and seeded

Type "y" if you want to write the document and press enter: y
Writing fields to output.txt...
Done! Fields have been written to output.txt
```

## Note!
Ensure you understand the impact of these operations as they can delete existing data. Always back up your database if needed before performing these actions.
