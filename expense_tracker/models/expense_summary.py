from dataclasses import dataclass


@dataclass
class ExpenseSummary:
    """Class to represent expense summary by category"""
    category: str
    amount: float
