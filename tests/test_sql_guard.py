"""
WhisperBase
File: test_sql_guard.py

Purpose:
Contains unit tests for SQL query validation and database protection logic.
"""

import sqlite3
from src.schema_scout import SchemaScout
from src.sql_guard import SQLGuard


def setup_database():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            city TEXT
        )
    """)

    connection.commit()
    return connection


def test_valid_select_query():
    connection = setup_database()
    schema_scout = SchemaScout(connection)
    sql_guard = SQLGuard(schema_scout)

    is_valid, message = sql_guard.validate_query("SELECT name, city FROM customers")

    assert is_valid is True
    assert message == "Query is valid"


def test_reject_non_select_query():
    connection = setup_database()
    schema_scout = SchemaScout(connection)
    sql_guard = SQLGuard(schema_scout)

    is_valid, message = sql_guard.validate_query("DROP TABLE customers")

    assert is_valid is False
    assert message == "Only SELECT queries are allowed"


def test_reject_unknown_table():
    connection = setup_database()
    schema_scout = SchemaScout(connection)
    sql_guard = SQLGuard(schema_scout)

    is_valid, message = sql_guard.validate_query("SELECT name FROM orders")

    assert is_valid is False
    assert "Unknown table" in message


def test_reject_unknown_column():
    connection = setup_database()
    schema_scout = SchemaScout(connection)
    sql_guard = SQLGuard(schema_scout)

    is_valid, message = sql_guard.validate_query("SELECT salary FROM customers")

    assert is_valid is False
    assert "Unknown column" in message


def test_reject_multiple_statements():
    connection = setup_database()
    schema_scout = SchemaScout(connection)
    sql_guard = SQLGuard(schema_scout)

    is_valid, message = sql_guard.validate_query("SELECT * FROM customers; DROP TABLE customers;")

    assert is_valid is False
    assert message == "Multiple SQL statements are not allowed"