from datetime import datetime
from expense_tracker.utils import Utils


class Expense:
    """This class represents an expense entry in the expense tracker application."""

    def __init__(
            self,
            amount: float,
            description: str,
            date: datetime = datetime.now(),
            category: str | None = None,
            id: int | None = None
    ):
        self.id = id
        self.amount = amount
        self.description = description
        self.date = date
        self.category = category if category is not None else Utils.auto_categorise(
            description)

    def __repr__(self):
        return f"{self.id}. {Utils.format_currency(self.amount)} \
for {self.description} on {self.date.isoformat()}. [{self.category}]"

    def to_dict(self):
        """Convert the Expense object to a dictionary representation."""
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "date": self.date.isoformat(),
            "category": self.category
        }

    def to_csv(self):
        """Convert Expense object to CSV format"""
        return f"{self.id},{self.amount},{self.description},{self.category},{self.date.isoformat()}"

    @staticmethod
    def from_dict(data: dict[str, any]):
        """Create an Expense object from a dictionary representation."""
        return Expense(data["amount"], data["description"], data["date"], data["category"], data.get("id"))
