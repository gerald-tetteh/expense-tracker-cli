import os
import json

import pytest

from expense_tracker.models.expense import Expense
from expense_tracker.models.exceptions import InvalidImportFileError
from datetime import datetime


class TestExpense:
    IMPORT_FILE = "test_parse"

    def teardown_method(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)

    def test_should_convert_to_dic(self):
        current_date = datetime.now()
        expense = Expense(50.0, "Groceries",
                          date=current_date, category="Food")
        expense_dict = expense.to_dict()
        assert expense_dict["amount"] == 50.0
        assert expense_dict["description"] == "Groceries"
        assert expense_dict["category"] == "Food"
        assert expense_dict["date"] == current_date.isoformat()

    def test_should_create_from_dic(self):
        current_date = datetime.now()
        expense_data = {
            "amount": 75.0,
            "description": "Utilities",
            "date": current_date,
            "category": "Bills"
        }
        expense = Expense.from_dict(expense_data)
        assert expense.amount == 75.0
        assert expense.description == "Utilities"
        assert expense.category == "Bills"
        assert expense.date == current_date

    def test_should_populate_category_and_date(self):
        expense = Expense(20.0, "Snacks")
        assert expense.category is not None
        assert isinstance(expense.date, datetime)

    def test_should_convert_to_csv(self):
        current_date = datetime.now()
        expense = Expense(50.0, "Groceries",
                          date=current_date, category="Food", id=1)
        expense_csv = expense.to_csv()
        assert f"1,50.0,Groceries,Food,{current_date.isoformat()}" == expense_csv

    def test_parse_csv(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)
        with open(self.IMPORT_FILE, "x") as file:
            file.writelines([
                "amount,description,category,date\n",
                "33.5,This is a test,Food,2025-05-12T12:00:00\n",
                "33.5,This is a test,Transport,2025-05-12T12:00:00\n",
                "33.5,This is a test,Entertainment,2025-05-12T12:00:00\n",
                "33.5,This is a test,Health,2025-05-12T12:00:00\n",
            ])
        expenses = Expense.parse_csv(self.IMPORT_FILE)
        assert len(expenses) == 4
        for expense in expenses:
            assert isinstance(expense, Expense)
            assert expense.date.isoformat() == "2025-05-12T12:00:00"
            assert isinstance(expense.amount, float)

    def test_parse_csv_throws_exception_on_invalid_field_type(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)
        with open(self.IMPORT_FILE, "x") as file:
            file.writelines([
                "amount,description,category,date\n",
                "et,This is a test,Food,2025-05-12T12:00:00\n",
                "33.5,This is a test,Transport,2025-05-12T12:00:00\n",
                "55.r,This is a test,Entertainment,2025-05-12T12:00:00\n",
                "33.5,This is a test,Health,2025-05-12T12:00:00\n",
            ])
        with pytest.raises(InvalidImportFileError) as ex:
            Expense.parse_csv(self.IMPORT_FILE)
        assert "Some fields may not be of the right type" in str(ex.value)

    def test_parse_csv_throws_exception_on_malformed_headings(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)
        with open(self.IMPORT_FILE, "x") as file:
            file.writelines([
                "amount,descrip,category,date\n",
                "33.5,This is a test,Food,2025-05-12T12:00:00\n",
                "33.5,This is a test,Transport,2025-05-12T12:00:00\n",
                "55.3,This is a test,Entertainment,2025-05-12T12:00:00\n",
                "33.5,This is a test,Health,2025-05-12T12:00:00\n",
            ])
        with pytest.raises(InvalidImportFileError) as ex:
            Expense.parse_csv(self.IMPORT_FILE)
        assert "Some column headings are malformed" in str(ex.value)

    def test_parse_csv_throws_exception_on_missing_file(self):
        with pytest.raises(InvalidImportFileError) as ex:
            Expense.parse_csv(self.IMPORT_FILE)
        assert "Import file does not exist" in str(ex.value)

    def test_parse_json_list(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)
        with open(self.IMPORT_FILE, "x") as file:
            current_date = datetime.now()
            expense = {
                "id": None,
                "amount": 75.0,
                "description": "Utilities",
                "date": current_date.isoformat(),
                "category": "Bills"
            }
            file.write(json.dumps([expense]))
        expenses = Expense.parse_json(self.IMPORT_FILE)
        assert isinstance(expenses, list)
        assert len(expenses) == 1
        assert expenses[0].to_dict() == expense

    def test_parse_json_single(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)
        with open(self.IMPORT_FILE, "x") as file:
            current_date = datetime.now()
            expense = {
                "id": None,
                "amount": 75.0,
                "description": "Utilities",
                "date": current_date.isoformat(),
                "category": "Bills"
            }
            file.write(json.dumps(expense))
        expenses = Expense.parse_json(self.IMPORT_FILE)
        assert isinstance(expenses, list)
        assert len(expenses) == 1
        assert expenses[0].to_dict() == expense

    def test_parse_json_should_throw_exception_on_missing_file(self):
        with pytest.raises(InvalidImportFileError) as ex:
            Expense.parse_json(self.IMPORT_FILE)
        assert "Import file does not exist" in str(ex.value)

    def test_parse_json_should_throw_exception_on_invalid_json(self):
        if os.path.exists(self.IMPORT_FILE):
            os.remove(self.IMPORT_FILE)
        with open(self.IMPORT_FILE, "x") as file:
            file.write(
                '{"amount": 75"description": "This is a test","date": "2025-06-12T12:00:00","category": "Food"}')
        with pytest.raises(InvalidImportFileError) as ex:
            Expense.parse_json(self.IMPORT_FILE)
        assert "File does not contain valid json" in str(ex.value)
