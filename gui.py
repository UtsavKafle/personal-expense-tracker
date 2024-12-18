import tkinter as tk
from tkinter import ttk, messagebox
from dataHandler import ExpenseDataHandler
from charts import ExpenseCharts


class ExpenseTrackerApp:
    def __init__(self, root):
        self.handler = ExpenseDataHandler()
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")  # Set the window size
        self.root.resizable(False, False)  # Disable resizing
        
        # Apply a ttk theme
        style = ttk.Style()
        style.theme_use("clam")  # Change theme for a modern look
        
        # Available categories
        self.categories = ["Food", "Travel", "Entertainment", "Groceries", "Utilities", "Other"]

        # Create the main GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Frame for inputs
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.grid(row=0, column=0, columnspan=2, sticky="w")

        # Input fields
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.category_combobox = ttk.Combobox(input_frame, values=self.categories, state="readonly", width=15)
        self.category_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.category_combobox.set("Select")

        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.desc_entry = ttk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        ttk.Button(button_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="View Report", command=self.view_report).grid(row=0, column=2, padx=10, pady=10)

        # Expense table with scrollbars
        table_frame = ttk.Frame(self.root, padding=10)
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.tree = ttk.Treeview(
            table_frame, columns=("Date", "Category", "Amount", "Description"), show="headings", height=15
        )
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.column("Date", anchor="center", width=100)
        self.tree.column("Category", anchor="center", width=100)
        self.tree.column("Amount", anchor="center", width=80)
        self.tree.column("Description", anchor="w", width=300)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=y_scrollbar.set, xscroll=x_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.load_expenses()

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_combobox.get()
        amount = self.amount_entry.get()
        description = self.desc_entry.get()

        if not date or category == "Select" or not amount:
            messagebox.showerror("Error", "Date, Category, and Amount are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return

        self.handler.add_expense(date, category, amount, description)
        self.load_expenses()

    def load_expenses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = self.handler.get_expenses()
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=(row["Date"], row["Category"], row["Amount"], row["Description"]))

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected!")
            return

        index = self.tree.index(selected_item[0])
        self.handler.delete_expense(index)
        self.load_expenses()

    def view_report(self):
        ExpenseCharts.generate_category_pie_chart()
