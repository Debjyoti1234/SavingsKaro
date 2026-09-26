from database import get_connection
from datetime import date


class Analytics:

    # ==========================================================
    # TOTAL INCOME, EXPENSE AND BALANCE
    # ==========================================================

    def get_totals(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Income'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                ),

                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Expense'
                            THEN amount
                            ELSE 0
                        END
                    ),
                    0
                )

            FROM transactions
        """)

        income, expense = cursor.fetchone()

        connection.close()

        balance = income - expense

        return income, expense, balance

    # ==========================================================
    # EXPENSES BY CATEGORY
    # ==========================================================

    def category_expenses(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE transaction_type = 'Expense'
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        data = cursor.fetchall()

        connection.close()

        return data

    # ==========================================================
    # CURRENT MONTH
    # ==========================================================

    def get_current_month(self):

        return date.today().strftime("%Y-%m")

    # ==========================================================
    # CURRENT MONTH EXPENSE
    # ==========================================================

    def get_monthly_expense(self):

        current_month = self.get_current_month()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 1, 7) = ?
        """, (
            current_month,
        ))

        result = cursor.fetchone()

        connection.close()

        return result[0]

    # ==========================================================
    # CURRENT MONTH BUDGET
    # ==========================================================

    def get_monthly_budget(self):

        from database import get_budget

        current_month = self.get_current_month()

        return get_budget(current_month)

    # ==========================================================
    # BUDGET SUMMARY
    # ==========================================================

    def get_budget_summary(self):

        budget = self.get_monthly_budget()

        expense = self.get_monthly_expense()

        if budget > 0:

            remaining = budget - expense

            percentage = (
                expense / budget
            ) * 100

        else:

            remaining = 0
            percentage = 0

        return (
            budget,
            expense,
            remaining,
            percentage
        )