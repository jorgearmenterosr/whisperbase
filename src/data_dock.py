"""
WhisperBase
File: data_dock.py

Purpose:
Loads structured CSV data into the SQLite database by inferring column
types, creating tables manually, and inserting rows without using df.to_sql().

AI Usage:
AI was used to help refine CSV loading logic and schema creation ideas.
All submitted code was reviewed, tested, and understood before submission.
"""

import pandas as pd


class DataDock:
    def __init__(self, connection):
        # Save the database connection and cursor for later use
        self.connection = connection
        self.cursor = connection.cursor()

    def infer_sql_type(self, dtype):
        # Map pandas data types to basic SQLite data types
        if "int" in str(dtype):
            return "INTEGER"
        elif "float" in str(dtype):
            return "REAL"
        else:
            return "TEXT"

    def create_table_from_csv(self, csv_file, table_name):
        # Read the CSV file into a pandas dataframe
        dataframe = pd.read_csv(csv_file)

        # Build the list of SQL column definitions
        columns = []
        for column_name, dtype in dataframe.dtypes.items():
            sql_type = self.infer_sql_type(dtype)
            columns.append(f"{column_name} {sql_type}")

        # Join all column definitions into one SQL string
        columns_sql = ", ".join(columns)

        # Create the table manually and add an auto-incrementing id column
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns_sql}
        )
        """

        # Execute the CREATE TABLE statement
        self.cursor.execute(create_table_query)
        self.connection.commit()

        # Return the dataframe so it can be inserted later
        return dataframe

    def insert_csv_data(self, dataframe, table_name):
        # Insert each row from the dataframe into the target table
        for _, row in dataframe.iterrows():
            column_names = ", ".join(dataframe.columns)
            placeholders = ", ".join(["?"] * len(dataframe.columns))

            insert_query = f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders})
            """

            # Use parameterized values to safely insert the row
            self.cursor.execute(insert_query, tuple(row))

        # Save all inserted rows
        self.connection.commit()

    def load_csv_to_database(self, csv_file, table_name):
        # Create the table structure from the CSV
        dataframe = self.create_table_from_csv(csv_file, table_name)

        # Insert the CSV rows into the new table
        self.insert_csv_data(dataframe, table_name)

        return f"Loaded {len(dataframe)} rows into table '{table_name}'"