import os
import pytest
from expense_tracker.db.db_client import DBClient
from expense_tracker.config import Config
from expense_tracker.models.exceptions import DBNotInitializedError


class TestDBClient:

    def setup_method(self):
        self.expenses = [
            {
                "id": 1,
                "amount": 50.0,
                "description": "Groceries",
                "date": "2024-10-01T12:00:00",
                "category": "Food"
            },
            {
                "id": 2,
                "amount": 62.3,
                "description": "Games",
                "date": "2024-10-02T12:00:00",
                "category": "Entertainment"
            },
            {
                "id": 3,
                "amount": 162.3,
                "description": "Bread",
                "date": "2024-07-02T12:00:00",
                "category": "Food"
            }
        ]
        os.environ[Config.ENV_DB_NAME] = "test_expenses.db"

    def teardown_method(self):
        # the tuple returned by PRAGMA database_list has the format (seq, name, file)
        db_path = DBClient.get_connection().execute(
            "PRAGMA database_list;").fetchone()[2]
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_init_db(self):
        DBClient.init_db()
        tables = DBClient.get_tables()
        assert len(tables) == 1
        assert "expenses" in tables

    def test_add_db_extension_on_init_db(self):
        os.environ[Config.ENV_DB_NAME] = "test_expenses"
        DBClient.init_db()
        connection = DBClient.get_connection()
        cursor = connection.cursor()
        cursor.execute("PRAGMA database_list;")
        db_list = cursor.fetchall()
        assert len(db_list) == 1
        db_file = db_list[0][2]
        assert db_file.endswith(".db")

    def test_get_connection_should_raise_error_if_db_name_not_set(self):
        del os.environ[Config.ENV_DB_NAME]
        with pytest.raises(ValueError) as ex:
            DBClient.get_connection()
        assert str(
            ex.value) == f"{Config.ENV_DB_NAME} environment variable is not set."
        os.environ[Config.ENV_DB_NAME] = "test_expenses.db"

    def test_add_expense(self):
        DBClient.init_db()
        expense_data = {
            "amount": 50.0,
            "description": "Groceries",
            "date": "2024-10-01T12:00:00",
            "category": "Food"
        }
        DBClient.add(expense_data)
        with DBClient.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT amount, description, date, category FROM expenses;")
            row = cursor.fetchone()
            assert row == (50.0, "Groceries", "2024-10-01T12:00:00", "Food")

    def test_add_expense_should_raise_error_if_db_not_initialized(self):
        expense_data = {
            "amount": 50.0,
            "description": "Groceries",
            "date": "2024-10-01T12:00:00",
            "category": "Food"
        }
        with pytest.raises(DBNotInitializedError) as ex:
            DBClient.add(expense_data)
        assert "Database is not initialized. Please run the init command." == str(
            ex.value)

    def test_list_expenses(self):
        DBClient.init_db()
        for expense in self.expenses:
            DBClient.add(expense)
        returned_expenses = DBClient.list_expenses("10", "2024")
        assert len(returned_expenses) == 2
        for (returned_expense, expected_expense) in zip(returned_expenses, self.expenses[0:2]):
            assert returned_expense.to_dict() == expected_expense

    def test_list_expense_should_paginate_expenses(self):
        DBClient.init_db()
        for expense in self.expenses:
            DBClient.add(expense)
        returned_expenses = DBClient.list_expenses("10", "2024", 1, 1)
        assert len(returned_expenses) == 1
        returned_expenses = DBClient.list_expenses("10", "2024", 2, 3)
        assert len(returned_expenses) == 0
