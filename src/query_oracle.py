"""
Receives SQL or natural language requests, validates them, executes
safe queries, and returns the results.

AI was used to help improve service structure and module interaction.
All code was reviewed and understood before submission.
"""

class QueryOracle:
    def __init__(self, connection, sql_guard, prompt_bridge):
        # Save the shared database connection and helper modules
        self.connection = connection
        self.cursor = connection.cursor()
        self.sql_guard = sql_guard
        self.prompt_bridge = prompt_bridge

    def run_sql_query(self, query):
        # Validate the query before any execution happens
        is_valid, message = self.sql_guard.validate_query(query)

        if not is_valid:
            return {"success": False, "message": message, "results": []}

        try:
            # Execute the validated query and fetch all matching rows
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            return {
                "success": True,
                "message": "Query executed successfully",
                "results": rows
            }
        except Exception as error:
            # Return the database error without crashing the program
            return {"success": False, "message": str(error), "results": []}

    def run_natural_language_query(self, user_request):
        # Convert the natural language request into SQL first
        generated_sql = self.prompt_bridge.generate_sql(user_request)

        # Validate and execute the generated SQL using the same safe flow
        result = self.run_sql_query(generated_sql)

        # Include the generated SQL in the returned response
        result["generated_sql"] = generated_sql
        return result
