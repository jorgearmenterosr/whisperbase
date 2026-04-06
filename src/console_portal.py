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
        # Save the main objects used by the CLI
        self.data_dock = data_dock
        self.query_oracle = query_oracle

    def show_menu(self):
        # Display the main CLI options
        print("\nWhisperBase Menu")
        print("1. Load CSV into database")
        print("2. Run SQL query")
        print("3. Ask natural language question")
        print("4. Exit")

    def load_csv_flow(self):
        # Ask the user for the CSV path and desired table name
        csv_file = input("Enter CSV file path: ").strip()
        table_name = input("Enter table name: ").strip()

        try:
            # Load the CSV into the database and print the result
            message = self.data_dock.load_csv_to_database(csv_file, table_name)
            print(message)
        except Exception as error:
            # Show an error instead of crashing the program
            print(f"Error: {error}")

    def sql_query_flow(self):
        # Ask the user for a raw SQL query
        query = input("Enter SQL query: ").strip()

        # Run the query through the safe query service
        result = self.query_oracle.run_sql_query(query)

        print(result["message"])
        if result["success"]:
            for row in result["results"]:
                print(row)

    def natural_language_flow(self):
        # Ask the user for a natural language request
        user_request = input("Ask your question: ").strip()

        # Convert it to SQL, validate it, and run it
        result = self.query_oracle.run_natural_language_query(user_request)

        print(f"Generated SQL: {result['generated_sql']}")
        print(result["message"])

        if result["success"]:
            for row in result["results"]:
                print(row)

    def run(self):
        # Keep showing the menu until the user decides to exit
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