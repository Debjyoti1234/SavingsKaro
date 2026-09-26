from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_type: str
    amount: float
    category: str
    description: str
    date: str