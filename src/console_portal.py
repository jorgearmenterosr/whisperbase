"""
WhisperBase
File: console_portal.py

Purpose:
Provides the command-line interface for loading CSV files, running SQL
queries, asking natural language questions, and exiting the program.

AI Usage:
AI was used to help refine CLI flow and interaction design.
All submitted code was reviewed, tested, and understood before submission.
"""

class ConsolePortal:
    def __init__(self, data_dock, query_oracle):
        self.data_dock = data_dock
        self.query_oracle = query_oracle

    def show_menu(self):
        print("\nWhisperBase Menu")
        print("1. Load CSV into database")
        print("2. Run SQL query")
        print("3. Ask natural language question")
        print("4. Exit")

    def load_csv_flow(self):
        csv_file = input("Enter CSV file path: ").strip()
        table_name = input("Enter table name: ").strip()

        try:
            message = self.data_dock.load_csv_to_database(csv_file, table_name)
            print(message)
        except Exception as error:
            print(f"Error: {error}")

    def sql_query_flow(self):
        query = input("Enter SQL query: ").strip()
        result = self.query_oracle.run_sql_query(query)

        print(result["message"])
        if result["success"]:
            for row in result["results"]:
                print(row)

    def natural_language_flow(self):
        user_request = input("Ask your question: ").strip()
        result = self.query_oracle.run_natural_language_query(user_request)

        print(f"Generated SQL: {result['generated_sql']}")
        print(result["message"])

        if result["success"]:
            for row in result["results"]:
                print(row)

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.load_csv_flow()
            elif choice == "2":
                self.sql_query_flow()
            elif choice == "3":
                self.natural_language_flow()
            elif choice == "4":
                print("Exiting WhisperBase.")
                break
            else:
                print("Invalid option. Please try again.")