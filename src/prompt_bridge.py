"""
Converts natural language questions into SQL queries using the database
schema and language model responses.

AI was used to help improve prompt structure and language handling.
All code was reviewed and understood before submission.
"""

class PromptBridge:
    def __init__(self, schema_scout):
        # Save the schema helper so prompts can include table information
        self.schema_scout = schema_scout

    def build_schema_context(self):
        # Get all current tables in the database
        tables = self.schema_scout.list_tables()
        context_lines = []

        # Build a readable description of each table and its columns
        for table in tables:
            schema = self.schema_scout.get_table_schema(table)
            columns = ", ".join([f"{name} ({dtype})" for name, dtype in schema.items()])
            context_lines.append(f"Table: {table} -> Columns: {columns}")

        return "\n".join(context_lines)

    def build_prompt(self, user_request):
        # Include schema context so the model knows what it can query
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
        # Build the prompt, even if the current version uses a simple fallback rule
        prompt = self.build_prompt(user_request)

        # Very simple placeholder rule for common input like "show all from customers"
        if "all" in user_request.lower() and "from" in user_request.lower():
            parts = user_request.lower().split("from")
            table_name = parts[-1].strip().replace(" ", "_")
            return f"SELECT * FROM {table_name}"

        # Default fallback query for unsupported requests
        return "SELECT 1"
