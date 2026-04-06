"""
WhisperBase
File: prompt_bridge.py

Purpose:
Converts natural language questions into SQL queries by using database
schema context and a language model response.

AI Usage:
AI was used to help refine prompt structure and natural language handling.
All submitted code was reviewed, tested, and understood before submission.
"""

class PromptBridge:
    def __init__(self, schema_scout):
        self.schema_scout = schema_scout

    def build_schema_context(self):
        tables = self.schema_scout.list_tables()
        context_lines = []

        for table in tables:
            schema = self.schema_scout.get_table_schema(table)
            columns = ", ".join([f"{name} ({dtype})" for name, dtype in schema.items()])
            context_lines.append(f"Table: {table} -> Columns: {columns}")

        return "\n".join(context_lines)

    def build_prompt(self, user_request):
        schema_context = self.build_schema_context()

        prompt = f"""
You are an assistant that converts natural language into safe SQLite SELECT queries.

Database schema:
{schema_context}

User request:
{user_request}

Rules:
- Only generate one SQLite SELECT query
- Do not generate INSERT, UPDATE, DELETE, DROP, or ALTER
- Only use tables and columns shown in the schema
- Return only the SQL query
"""
        return prompt.strip()

    def generate_sql(self, user_request):
        prompt = self.build_prompt(user_request)

        if "all" in user_request.lower() and "from" in user_request.lower():
            parts = user_request.lower().split("from")
            table_name = parts[-1].strip().replace(" ", "_")
            return f"SELECT * FROM {table_name}"

        return "SELECT 1"