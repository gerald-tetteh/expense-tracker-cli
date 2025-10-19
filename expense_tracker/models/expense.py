from datetime import datetime


class Expense:
    """This class represents an expense entry in the expense tracker application."""

    def __init__(self, amount: float, description: str, date: datetime = datetime.now(), category: str = "None"):
        self.amount = amount
        self.description = description
        self.date = date
        self.category = category  # TODO: Implement category assignment logic

    def __repr__(self):
        return f"Expense(amount={self.amount}, description='{self.description}', date='{self.date}', category='{self.category}')"

    def to_dict(self):
        """Convert the Expense object to a dictionary representation."""
        return {
            "amount": self.amount,
            "description": self.description,
            "date": self.date.isoformat(),
            "category": self.category
        }

    @staticmethod
    def from_dict(data: dict[str, any]):
        """Create an Expense object from a dictionary representation."""
        return Expense(data["amount"], data["description"], data["date"], data["category"])
