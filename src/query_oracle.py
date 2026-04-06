"""
WhisperBase
File: query_oracle.py

Purpose:
Acts as the main query service layer by receiving SQL or natural language
requests, validating them, executing safe queries, and returning results.

AI Usage:
AI was used to help refine service structure and module interaction.
All submitted code was reviewed, tested, and understood before submission.
"""

class QueryOracle:
    def __init__(self, connection, sql_guard, prompt_bridge):
        self.connection = connection
        self.cursor = connection.cursor()
        self.sql_guard = sql_guard
        self.prompt_bridge = prompt_bridge

    def run_sql_query(self, query):
        is_valid, message = self.sql_guard.validate_query(query)

        if not is_valid:
            return {"success": False, "message": message, "results": []}

        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return {"success": True, "message": "Query executed successfully", "results": rows}
        except Exception as error:
            return {"success": False, "message": str(error), "results": []}

    def run_natural_language_query(self, user_request):
        generated_sql = self.prompt_bridge.generate_sql(user_request)
        result = self.run_sql_query(generated_sql)
        result["generated_sql"] = generated_sql
        return result