import matplotlib.pyplot as plt
import pandas as pd

class ExpenseCharts:
    @staticmethod
    def generate_category_pie_chart(file_name="expenses.csv"):
        df = pd.read_csv(file_name)
        category_totals = df.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(8, 6))
        category_totals.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.ylabel("")
        plt.show()
