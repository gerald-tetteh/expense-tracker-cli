from expense_tracker.models.expense import Expense
from datetime import datetime


class TestExpense:
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
        assert f"1,50.0,Groceries,Food,{current_date.isoformat()}"
