"""
WhisperBase
File: main.py

Purpose:
Connects all WhisperBase modules together and starts the command-line interface.

AI Usage:
AI was used to help refine project structure and module organization.
All submitted code was reviewed, tested, and understood before submission.
"""

from src.db_engine import DatabaseEngine
from src.data_dock import DataDock
from src.schema_scout import SchemaScout
from src.sql_guard import SQLGuard
from src.prompt_bridge import PromptBridge
from src.query_oracle import QueryOracle
from src.console_portal import ConsolePortal


def main():
    database_engine = DatabaseEngine()
    connection = database_engine.connect()

    data_dock = DataDock(connection)
    schema_scout = SchemaScout(connection)
    sql_guard = SQLGuard(schema_scout)
    prompt_bridge = PromptBridge(schema_scout)
    query_oracle = QueryOracle(connection, sql_guard, prompt_bridge)
    console_portal = ConsolePortal(data_dock, query_oracle)

    console_portal.run()
    connection.close()


if __name__ == "__main__":
    main()