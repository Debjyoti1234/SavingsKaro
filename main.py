import tkinter as tk

from database import initialize_database
from ui import ExpenseTrackerApp


def main():
    initialize_database()

    root = tk.Tk()

    app = ExpenseTrackerApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()