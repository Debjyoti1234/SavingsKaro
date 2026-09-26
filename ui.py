import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import csv

from models import Transaction
from expense_manager import ExpenseManager
from analytics import Analytics
from database import save_budget


class ExpenseTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("SmartSpend - Expense Tracker")
        self.root.geometry("1150x780")
        self.root.minsize(1000, 650)

        self.manager = ExpenseManager()
        self.analytics = Analytics()

        # ==============================
        # CATEGORIES
        # ==============================

        self.expense_categories = [
            "Food",
            "Transport",
            "Education",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Other"
        ]

        self.income_categories = [
            "Salary",
            "Freelance",
            "Scholarship",
            "Pocket Money",
            "Business",
            "Other"
        ]

        self.create_widgets()
        self.refresh_data()

    # ==============================
    # CREATE GUI
    # ==============================

    def create_widgets(self):

        # ------------------------------
        # TITLE
        # ------------------------------

        title = tk.Label(
            self.root,
            text="SmartSpend",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(15, 2))

        subtitle = tk.Label(
            self.root,
            text="Personal Expense & Budget Tracker",
            font=("Arial", 11)
        )
        subtitle.pack()

        # ------------------------------
        # DASHBOARD
        # ------------------------------

        dashboard = tk.Frame(self.root)
        dashboard.pack(pady=12)

        self.income_label = tk.Label(
            dashboard,
            text="Income\n₹0.00",
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        self.income_label.grid(
            row=0,
            column=0,
            padx=10
        )

        self.expense_label = tk.Label(
            dashboard,
            text="Expenses\n₹0.00",
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        self.expense_label.grid(
            row=0,
            column=1,
            padx=10
        )

        self.balance_label = tk.Label(
            dashboard,
            text="Balance\n₹0.00",
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        self.balance_label.grid(
            row=0,
            column=2,
            padx=10
        )

        # ------------------------------
        # MONTHLY BUDGET
        # ------------------------------

        budget_frame = tk.LabelFrame(
            self.root,
            text="Monthly Budget",
            padx=15,
            pady=8
        )

        budget_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            budget_frame,
            text="Set Budget:"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.budget_entry = tk.Entry(
            budget_frame,
            width=15
        )

        self.budget_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            budget_frame,
            text="Set Budget",
            command=self.set_budget
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.budget_info = tk.Label(
            budget_frame,
            text="Budget: ₹0.00   Spent: ₹0.00   Remaining: ₹0.00",
            font=("Arial", 11, "bold")
        )

        self.budget_info.grid(
            row=0,
            column=3,
            padx=20
        )

        self.progress = ttk.Progressbar(
            budget_frame,
            orient="horizontal",
            length=350,
            mode="determinate",
            maximum=100
        )

        self.progress.grid(
            row=1,
            column=0,
            columnspan=4,
            pady=8
        )

        self.budget_status = tk.Label(
            budget_frame,
            text="No monthly budget set",
            font=("Arial", 10, "bold")
        )

        self.budget_status.grid(
            row=2,
            column=0,
            columnspan=4
        )

        # ------------------------------
        # ADD / EDIT TRANSACTION
        # ------------------------------

        form = tk.LabelFrame(
            self.root,
            text="Add / Edit Transaction",
            padx=10,
            pady=8
        )

        form.pack(
            fill="x",
            padx=20,
            pady=8
        )

        # Type

        tk.Label(
            form,
            text="Type"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.type_box = ttk.Combobox(
            form,
            values=[
                "Income",
                "Expense"
            ],
            state="readonly",
            width=12
        )

        self.type_box.set("Expense")

        self.type_box.grid(
            row=0,
            column=1,
            padx=5
        )

        self.type_box.bind(
            "<<ComboboxSelected>>",
            self.update_categories
        )

        # Amount

        tk.Label(
            form,
            text="Amount"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.amount_entry = tk.Entry(
            form,
            width=15
        )

        self.amount_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        # Category

        tk.Label(
            form,
            text="Category"
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        self.category_box = ttk.Combobox(
            form,
            values=self.expense_categories,
            state="readonly",
            width=15
        )

        self.category_box.set("Food")

        self.category_box.grid(
            row=0,
            column=5,
            padx=5
        )

        # Description

        tk.Label(
            form,
            text="Description"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=8
        )

        self.description_entry = tk.Entry(
            form,
            width=30
        )

        self.description_entry.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=5,
            pady=8
        )

        # Add button

        tk.Button(
            form,
            text="Add Transaction",
            command=self.add_transaction
        ).grid(
            row=1,
            column=5,
            padx=5
        )

        # Update button

        tk.Button(
            form,
            text="Update Selected",
            command=self.update_transaction
        ).grid(
            row=1,
            column=6,
            padx=5
        )

        # ------------------------------
        # SEARCH / FILTER
        # ------------------------------

        filter_frame = tk.Frame(self.root)

        filter_frame.pack(
            fill="x",
            padx=20,
            pady=4
        )

        tk.Label(
            filter_frame,
            text="Search:"
        ).pack(
            side="left",
            padx=5
        )

        self.search_entry = tk.Entry(
            filter_frame,
            width=25
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.filter_transactions()
        )

        tk.Label(
            filter_frame,
            text="Type:"
        ).pack(
            side="left",
            padx=5
        )

        self.filter_box = ttk.Combobox(
            filter_frame,
            values=[
                "All",
                "Income",
                "Expense"
            ],
            state="readonly",
            width=12
        )

        self.filter_box.set("All")

        self.filter_box.pack(
            side="left",
            padx=5
        )

        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.filter_transactions()
        )

        tk.Button(
            filter_frame,
            text="Clear",
            command=self.clear_filters
        ).pack(
            side="left",
            padx=5
        )

        # ------------------------------
        # TRANSACTION TABLE
        # ------------------------------

        table_frame = tk.Frame(self.root)

        table_frame.pack(
            fill="x",
            expand=False,
            padx=20,
            pady=5
        )

        columns = (
            "ID",
            "Type",
            "Amount",
            "Category",
            "Description",
            "Date"
        )

        # FIXED HEIGHT
        # This keeps the buttons below visible.

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        # Headings

        for column in columns:
            self.table.heading(
                column,
                text=column
            )

        # Column sizes

        self.table.column(
            "ID",
            width=50,
            anchor="center"
        )

        self.table.column(
            "Type",
            width=100,
            anchor="center"
        )

        self.table.column(
            "Amount",
            width=100,
            anchor="center"
        )

        self.table.column(
            "Category",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Description",
            width=280,
            anchor="w"
        )

        self.table.column(
            "Date",
            width=120,
            anchor="center"
        )

        # Scrollbar

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="x",
            expand=False
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_transaction
        )

        # ------------------------------
        # BOTTOM BUTTONS
        # ------------------------------

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=8
        )

        tk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_transaction,
            width=16
        ).pack(
            side="left",
            padx=8
        )

        tk.Button(
            button_frame,
            text="Expense Chart",
            command=self.show_chart,
            width=16
        ).pack(
            side="left",
            padx=8
        )

        tk.Button(
            button_frame,
            text="Export CSV",
            command=self.export_csv,
            width=16
        ).pack(
            side="left",
            padx=8
        )

    # ==============================
    # CATEGORY MANAGEMENT
    # ==============================

    def update_categories(self, event=None):

        transaction_type = self.type_box.get()

        if transaction_type == "Income":

            categories = self.income_categories

        else:

            categories = self.expense_categories

        self.category_box["values"] = categories

        self.category_box.set(
            categories[0]
        )

    # ==============================
    # ADD TRANSACTION
    # ==============================

    def add_transaction(self):

        try:

            amount = float(
                self.amount_entry.get()
            )

            if amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid positive amount."
            )

            return

        description = (
            self.description_entry
            .get()
            .strip()
        )

        if not description:

            messagebox.showwarning(
                "Missing Description",
                "Please enter a description."
            )

            return

        transaction = Transaction(
            transaction_type=self.type_box.get(),
            amount=amount,
            category=self.category_box.get(),
            description=description,
            date=date.today().isoformat()
        )

        self.manager.add_transaction(
            transaction
        )

        self.clear_form()
        self.refresh_data()

        messagebox.showinfo(
            "Success",
            "Transaction added successfully!"
        )

    # ==============================
    # LOAD SELECTED TRANSACTION
    # ==============================

    def load_selected_transaction(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        item = self.table.item(
            selected[0]
        )

        values = item["values"]

        self.type_box.set(
            values[1]
        )

        self.update_categories()

        self.category_box.set(
            values[3]
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.insert(
            0,
            values[2]
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.description_entry.insert(
            0,
            values[4]
        )

    # ==============================
    # UPDATE TRANSACTION
    # ==============================

    def update_transaction(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a transaction."
            )

            return

        item = self.table.item(
            selected[0]
        )

        values = item["values"]

        transaction_id = values[0]

        try:

            amount = float(
                self.amount_entry.get()
            )

            if amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid positive amount."
            )

            return

        description = (
            self.description_entry
            .get()
            .strip()
        )

        if not description:

            messagebox.showwarning(
                "Missing Description",
                "Please enter a description."
            )

            return

        transaction = Transaction(
            transaction_type=self.type_box.get(),
            amount=amount,
            category=self.category_box.get(),
            description=description,
            date=values[5]
        )

        self.manager.update_transaction(
            transaction_id,
            transaction
        )

        self.clear_form()
        self.refresh_data()

        messagebox.showinfo(
            "Updated",
            "Transaction updated successfully!"
        )

    # ==============================
    # DELETE TRANSACTION
    # ==============================

    def delete_transaction(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a transaction."
            )

            return

        item = self.table.item(
            selected[0]
        )

        transaction_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        self.manager.delete_transaction(
            transaction_id
        )

        self.clear_form()
        self.refresh_data()

    # ==============================
    # SET BUDGET
    # ==============================

    def set_budget(self):

        try:

            budget = float(
                self.budget_entry.get()
            )

            if budget <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Budget",
                "Please enter a valid positive budget."
            )

            return

        current_month = (
            self.analytics
            .get_current_month()
        )

        save_budget(
            current_month,
            budget
        )

        self.budget_entry.delete(
            0,
            tk.END
        )

        self.update_budget_display()

        messagebox.showinfo(
            "Budget Saved",
            f"Monthly budget set to ₹{budget:.2f}"
        )

    # ==============================
    # UPDATE BUDGET DISPLAY
    # ==============================

    def update_budget_display(self):

        (
            budget,
            expense,
            remaining,
            percentage
        ) = self.analytics.get_budget_summary()

        self.budget_info.config(
            text=(
                f"Budget: ₹{budget:.2f}   "
                f"Spent: ₹{expense:.2f}   "
                f"Remaining: ₹{remaining:.2f}"
            )
        )

        if budget <= 0:

            self.progress["value"] = 0

            self.budget_status.config(
                text="No monthly budget set"
            )

            return

        progress_value = min(
            percentage,
            100
        )

        self.progress["value"] = progress_value

        if expense > budget:

            self.budget_status.config(
                text=(
                    f"⚠ Budget exceeded by "
                    f"₹{abs(remaining):.2f}"
                )
            )

        elif percentage >= 80:

            self.budget_status.config(
                text=(
                    f"⚠ You have used "
                    f"{percentage:.1f}% of your budget"
                )
            )

        else:

            self.budget_status.config(
                text=(
                    f"✓ Within budget — "
                    f"{percentage:.1f}% used"
                )
            )

    # ==============================
    # REFRESH DATA
    # ==============================

    def refresh_data(self):

        transactions = (
            self.manager
            .get_transactions()
        )

        self.display_transactions(
            transactions
        )

        income, expense, balance = (
            self.analytics
            .get_totals()
        )

        self.income_label.config(
            text=f"Income\n₹{income:.2f}"
        )

        self.expense_label.config(
            text=f"Expenses\n₹{expense:.2f}"
        )

        self.balance_label.config(
            text=f"Balance\n₹{balance:.2f}"
        )

        self.update_budget_display()

    # ==============================
    # DISPLAY TRANSACTIONS
    # ==============================

    def display_transactions(
        self,
        transactions
    ):

        for item in self.table.get_children():

            self.table.delete(
                item
            )

        for transaction in transactions:

            self.table.insert(
                "",
                tk.END,
                values=transaction
            )

    # ==============================
    # SEARCH AND FILTER
    # ==============================

    def filter_transactions(self):

        search_text = (
            self.search_entry
            .get()
            .lower()
            .strip()
        )

        filter_type = (
            self.filter_box
            .get()
        )

        transactions = (
            self.manager
            .get_transactions()
        )

        filtered_transactions = []

        for transaction in transactions:

            transaction_type = str(
                transaction[1]
            )

            category = str(
                transaction[3]
            ).lower()

            description = str(
                transaction[4]
            ).lower()

            matches_search = (
                search_text in category
                or search_text in description
                or search_text in transaction_type.lower()
            )

            matches_filter = (
                filter_type == "All"
                or transaction_type == filter_type
            )

            if (
                matches_search
                and matches_filter
            ):

                filtered_transactions.append(
                    transaction
                )

        self.display_transactions(
            filtered_transactions
        )

    # ==============================
    # CLEAR FILTER
    # ==============================

    def clear_filters(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.filter_box.set(
            "All"
        )

        self.refresh_data()

    # ==============================
    # EXPENSE CHART
    # ==============================

    def show_chart(self):

        data = (
            self.analytics
            .category_expenses()
        )

        if not data:

            messagebox.showinfo(
                "No Data",
                "There are no expense records to display."
            )

            return

        try:

            import matplotlib.pyplot as plt

            categories = [
                row[0]
                for row in data
            ]

            amounts = [
                row[1]
                for row in data
            ]

            plt.figure(
                figsize=(9, 5)
            )

            plt.bar(
                categories,
                amounts
            )

            plt.title(
                "SmartSpend - Expenses by Category"
            )

            plt.xlabel(
                "Category"
            )

            plt.ylabel(
                "Amount (₹)"
            )

            plt.xticks(
                rotation=30
            )

            plt.tight_layout()

            plt.show()

        except ImportError:

            messagebox.showerror(
                "Matplotlib Missing",
                "Matplotlib is not installed.\n\n"
                "Run:\n"
                "pip install matplotlib"
            )

    # ==============================
    # EXPORT CSV
    # ==============================

    def export_csv(self):

        transactions = (
            self.manager
            .get_transactions()
        )

        if not transactions:

            messagebox.showinfo(
                "No Data",
                "There are no transactions to export."
            )

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                (
                    "CSV Files",
                    "*.csv"
                )
            ],
            title="Save Expense Report"
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow([
                    "ID",
                    "Type",
                    "Amount",
                    "Category",
                    "Description",
                    "Date"
                ])

                writer.writerows(
                    transactions
                )

            messagebox.showinfo(
                "Export Successful",
                "Transactions exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                f"Could not export file:\n{error}"
            )

    # ==============================
    # CLEAR FORM
    # ==============================

    def clear_form(self):

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.type_box.set(
            "Expense"
        )

        self.category_box["values"] = (
            self.expense_categories
        )

        self.category_box.set(
            "Food"
        )