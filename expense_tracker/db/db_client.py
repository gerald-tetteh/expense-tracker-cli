import sqlite3
import os
from pathlib import Path
from expense_tracker.config import Config

TABLE_NAME = "expenses"


class DBClient:

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """Get a connection to the SQLite database."""
        db_name = os.getenv(Config.ENV_DB_NAME)
        if db_name is None:
            raise ValueError("DB_NAME environment variable is not set.")
        if not db_name.endswith(".db"):
            db_name += ".db"
            os.environ[Config.ENV_DB_NAME] = db_name
        db_path = Path(__file__).parent / db_name
        return sqlite3.connect(db_path)

    @staticmethod
    def init_db():
        """Initialize the database connection and create the expenses table if it doesn't exist."""
        with DBClient.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            ''')
            connection.commit()

    @staticmethod
    def get_tables() -> list[str]:
        """Retrieve the list of tables in the database."""
        with DBClient.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row[0] for row in cursor.fetchall()]
            return tables

    @staticmethod
    def add(data: dict[str, any]):
        """Add a new expense entry to the database."""
        with DBClient.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                INSERT INTO {TABLE_NAME} (amount, description, date, category)
                VALUES (?, ?, ?, ?)
            ''', (data["amount"], data["description"], data["date"], data["category"]))
            connection.commit()
