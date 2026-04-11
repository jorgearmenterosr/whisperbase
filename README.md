# WhisperBase

WhisperBase is a Python project that loads CSV data into SQLite and allows users to query the database using either SQL or natural language.
PROJECT VIDEO LINK:
https://youtu.be/qUr7I-UxVrg

## Files

* main.py

  * Runs the project

* db_engine.py

  * Connects to the SQLite database

* data_dock.py

  * Loads CSV files into the database

* schema_scout.py

  * Checks database tables, columns, and data types

* sql_guard.py

  * Validates SQL queries before they run

* prompt_bridge.py

  * Converts natural language into SQL

* query_oracle.py

  * Handles query execution

* console_portal.py

  * Handles the command-line interface

* tests/

  * Contains test files

* data/

  * Contains sample CSV files

## What the Project Does

* Loads CSV files into SQLite
* Creates database tables
* Allows SQL queries
* Allows natural language queries
* Converts natural language into SQL
* Validates SQL before execution
* Prevents unsafe queries

## How to Run

```bash
python -m src.main
```

## How to Run Tests

```bash
pytest
```

## Author

Jorge Armenteros
Boston University EC530

