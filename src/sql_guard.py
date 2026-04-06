"""
WhisperBase
File: sql_guard.py

Purpose:
Validates SQL queries before execution by allowing only safe SELECT queries
and rejecting unsupported or unsafe database operations.

AI Usage:
AI was used to help refine SQL validation logic and security ideas.
All submitted code was reviewed, tested, and understood before submission.
"""

import re


class SQLGuard:
    def __init__(self, schema_scout):
        self.schema_scout = schema_scout

    def is_select_query(self, query):
        cleaned_query = query.strip().lower()
        return cleaned_query.startswith("select")

    def has_multiple_statements(self, query):
        statements = [part.strip() for part in query.split(";") if part.strip()]
        return len(statements) > 1

    def extract_table_names(self, query):
        query_lower = query.lower()
        tables = []

        from_matches = re.findall(r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)", query_lower)
        join_matches = re.findall(r"\bjoin\s+([a-zA-Z_][a-zA-Z0-9_]*)", query_lower)

        tables.extend(from_matches)
        tables.extend(join_matches)

        return list(set(tables))

    def extract_column_names(self, query):
        query_lower = query.lower()

        select_match = re.search(r"select\s+(.*?)\s+from\s", query_lower)
        if not select_match:
            return []

        column_text = select_match.group(1).strip()

        if column_text == "*":
            return ["*"]

        columns = []
        raw_columns = column_text.split(",")

        for column in raw_columns:
            cleaned_column = column.strip()

            if " as " in cleaned_column:
                cleaned_column = cleaned_column.split(" as ")[0].strip()

            if "." in cleaned_column:
                cleaned_column = cleaned_column.split(".")[-1].strip()

            columns.append(cleaned_column)

        return columns

    def validate_tables(self, query):
        table_names = self.extract_table_names(query)
        known_tables = self.schema_scout.list_tables()

        for table in table_names:
            if table not in known_tables:
                return False, f"Unknown table: {table}"

        return True, "Tables are valid"

    def validate_columns(self, query):
        table_names = self.extract_table_names(query)
        column_names = self.extract_column_names(query)

        if "*" in column_names:
            return True, "Wildcard column selection is valid"

        allowed_columns = set()

        for table in table_names:
            schema = self.schema_scout.get_table_schema(table)
            for column in schema.keys():
                allowed_columns.add(column.lower())

        for column in column_names:
            if column.lower() not in allowed_columns:
                return False, f"Unknown column: {column}"

        return True, "Columns are valid"

    def validate_query(self, query):
        if not self.is_select_query(query):
            return False, "Only SELECT queries are allowed"

        if self.has_multiple_statements(query):
            return False, "Multiple SQL statements are not allowed"

        tables_valid, table_message = self.validate_tables(query)
        if not tables_valid:
            return False, table_message

        columns_valid, column_message = self.validate_columns(query)
        if not columns_valid:
            return False, column_message

        return True, "Query is valid"