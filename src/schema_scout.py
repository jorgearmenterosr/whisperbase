"""
WhisperBase
File: schema_scout.py

Purpose:
Checks existing database tables, columns, and data types so the system
can understand the current schema and compare it with incoming CSV data.

AI Usage:
AI was used to help refine schema inspection and comparison ideas.
All submitted code was reviewed, tested, and understood before submission.
"""

class SchemaScout:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        self.cursor.execute(query)
        tables = [row[0] for row in self.cursor.fetchall()]
        return tables

    def get_table_schema(self, table_name):
        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        schema = {}
        for row in rows:
            column_name = row[1]
            column_type = row[2]
            if column_name != "id":
                schema[column_name] = column_type

        return schema

    def normalize_column_name(self, column_name):
        return column_name.strip().lower().replace(" ", "_")

    def compare_schema(self, csv_schema, table_schema):
        normalized_csv_schema = {
            self.normalize_column_name(column): dtype
            for column, dtype in csv_schema.items()
        }

        normalized_table_schema = {
            self.normalize_column_name(column): dtype
            for column, dtype in table_schema.items()
        }

        return normalized_csv_schema == normalized_table_schema

    def find_matching_table(self, csv_schema):
        tables = self.list_tables()

        for table in tables:
            table_schema = self.get_table_schema(table)
            if self.compare_schema(csv_schema, table_schema):
                return table

        return None