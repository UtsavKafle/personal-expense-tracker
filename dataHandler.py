import pandas as pd
import os

class ExpenseDataHandler:
    def __init__(self, file_name="expenses.csv"):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            self.create_file()

    def create_file(self):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(self.file_name, index=False)

    def add_expense(self, date, category, amount, description):
        df = pd.read_csv(self.file_name)
        new_expense = {"Date": date, "Category": category, "Amount": amount, "Description": description}
        df = df.append(new_expense, ignore_index=True)
        df.to_csv(self.file_name, index=False)

    def get_expenses(self):
        return pd.read_csv(self.file_name)

    def delete_expense(self, index):
        df = pd.read_csv(self.file_name)
        df = df.drop(index=index)
        df.to_csv(self.file_name, index=False)
