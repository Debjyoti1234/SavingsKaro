from database import get_connection


class ExpenseManager:

    # ==========================================================
    # ADD TRANSACTION
    # ==========================================================

    def add_transaction(self, transaction):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (transaction_type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction.transaction_type,
            transaction.amount,
            transaction.category,
            transaction.description,
            transaction.date
        ))

        connection.commit()
        connection.close()

    # ==========================================================
    # GET ALL TRANSACTIONS
    # ==========================================================

    def get_transactions(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                transaction_type,
                amount,
                category,
                description,
                date
            FROM transactions
            ORDER BY date DESC, id DESC
        """)

        rows = cursor.fetchall()

        connection.close()

        return rows

    # ==========================================================
    # DELETE TRANSACTION
    # ==========================================================

    def delete_transaction(self, transaction_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        connection.commit()
        connection.close()

    # ==========================================================
    # UPDATE TRANSACTION
    # ==========================================================

    def update_transaction(
        self,
        transaction_id,
        transaction
    ):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE transactions
            SET
                transaction_type = ?,
                amount = ?,
                category = ?,
                description = ?,
                date = ?
            WHERE id = ?
        """, (
            transaction.transaction_type,
            transaction.amount,
            transaction.category,
            transaction.description,
            transaction.date,
            transaction_id
        ))

        connection.commit()
        connection.close()