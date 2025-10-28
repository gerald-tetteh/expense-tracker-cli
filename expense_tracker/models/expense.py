from datetime import datetime
from csv import DictReader

from expense_tracker.utils import Utils
from .exceptions import InvalidImportFileError


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

    @staticmethod
    def parse_csv(file: str):
        """Parse expenses from csv file."""
        try:
            with open(file, "r") as csv_file:
                reader = DictReader(csv_file)
                reader.fieldnames = [name.lower()
                                     for name in reader.fieldnames]
                return [
                    Expense(
                        amount=float(row["amount"]),
                        category=row["category"],
                        date=datetime.fromisoformat(row["date"]),
                        description=row["description"],
                    )
                    for row in reader
                ]
        except ValueError:
            raise InvalidImportFileError(
                "Some fields may not be of the right type. 'amount' should be a number and 'date' is in the ISO format.")
        except KeyError:
            raise InvalidImportFileError(
                "Some column headings are malformed. The first row should contain the headings.")
        except FileNotFoundError:
            raise InvalidImportFileError("Import file does not exist")
        except Exception:
            raise RuntimeError("Could not parse file")
