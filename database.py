import sqlite3
from pathlib import Path


DB_PATH = Path("data/expense_tracker.db")


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    DB_PATH.parent.mkdir(exist_ok=True)

    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Create the required database tables if they do not exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    # Monthly budget table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_budget(month, amount):
    """
    Save a monthly budget.

    If a budget already exists for the month,
    update it instead of creating another one.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (month, amount)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount = excluded.amount
    """, (
        month,
        amount
    ))

    connection.commit()
    connection.close()


def get_budget(month):
    """
    Return the budget for a particular month.

    Returns 0 if no budget has been set.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount
        FROM budgets
        WHERE month = ?
    """, (
        month,
    ))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return 0