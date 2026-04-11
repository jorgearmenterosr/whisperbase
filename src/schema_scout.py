"""
Checks existing database tables, columns, and data types so the system
can understand the current schema.

AI was used to help improve schema inspection logic.
All code was reviewed and understood before submission.
"""

class SchemaScout:
    def __init__(self, connection):
        # Save the database connection and cursor
        self.connection = connection
        self.cursor = connection.cursor()

    def list_tables(self):
        # Get all user-created tables and ignore internal SQLite tables
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        self.cursor.execute(query)
        tables = [row[0] for row in self.cursor.fetchall()]
        return tables

    def get_table_schema(self, table_name):
        # Read the schema information for one table
        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Store column names and types in a dictionary
        schema = {}
        for row in rows:
            column_name = row[1]
            column_type = row[2]

            # Ignore the auto-generated id column during comparisons
            if column_name != "id":
                schema[column_name] = column_type

        return schema

    def normalize_column_name(self, column_name):
        # Normalize column names so comparisons are more consistent
        return column_name.strip().lower().replace(" ", "_")

    def compare_schema(self, csv_schema, table_schema):
        # Normalize both schemas before comparing them
        normalized_csv_schema = {
            self.normalize_column_name(column): dtype
            for column, dtype in csv_schema.items()
        }

        normalized_table_schema = {
            self.normalize_column_name(column): dtype
            for column, dtype in table_schema.items()
        }

        # Return True only if both schemas match exactly
        return normalized_csv_schema == normalized_table_schema

    def find_matching_table(self, csv_schema):
        # Look through all existing tables to find a schema match
        tables = self.list_tables()

        for table in tables:
            table_schema = self.get_table_schema(table)
            if self.compare_schema(csv_schema, table_schema):
                return table

        # Return None if no match is found
        return None
