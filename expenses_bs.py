import csv
import os


class ExpenseBS:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


def osszeg_bs(expense_list):
    total = 0
    for expense in expense_list:
        total += expense.amount
    return total


def save_expenses_to_csv_bs(expense_list, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["date", "category", "amount", "description"])
        for expense in expense_list:
            writer.writerow([expense.date, expense.category, expense.amount, expense.description])


def load_expenses_from_csv_bs(filename):
    expenses = []
    if not os.path.exists(filename):
        return expenses
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = True
        for row in reader:
            if header:
                header = False
                continue
            if len(row) != 4:
                continue
            date, category, amount_text, description = row
            try:
                amount = float(amount_text)
            except ValueError:
                continue
            expense = ExpenseBS(date, category, amount, description)
            expenses.append(expense)
    return expenses
