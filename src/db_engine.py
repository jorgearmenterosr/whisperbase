"""
WhisperBase
File: db_engine.py

Purpose:
Handles SQLite database connection setup and shared database utilities
used throughout the system.

AI Usage:
AI was used to help refine database utility structure and organization.
All submitted code was reviewed, tested, and understood before submission.
"""

import sqlite3


class DatabaseEngine:
    def __init__(self, db_name="whisperbase.db"):
        # Store the database file name
        self.db_name = db_name

    def connect(self):
        # Open and return a connection to the SQLite database
        connection = sqlite3.connect(self.db_name)
        return connection

    def get_cursor(self):
        # Create a connection and cursor together for convenience
        connection = self.connect()
        cursor = connection.cursor()
        return connection, cursor