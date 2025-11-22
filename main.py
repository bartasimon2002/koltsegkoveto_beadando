import tkinter as tk
from expenses_bs import ExpenseBS, osszeg_bs, save_expenses_to_csv_bs, load_expenses_from_csv_bs


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Költségkövető")
        self.expenses = []
        self.filename = "expenses_bs.csv"

        self.frame_inputs = tk.Frame(self.root)
        self.frame_inputs.pack(padx=10, pady=10)

        self.label_date = tk.Label(self.frame_inputs, text="Dátum")
        self.label_date.grid(row=0, column=0)
        self.entry_date = tk.Entry(self.frame_inputs)
        self.entry_date.grid(row=0, column=1)

        self.label_category = tk.Label(self.frame_inputs, text="Kategória")
        self.label_category.grid(row=1, column=0)
        self.entry_category = tk.Entry(self.frame_inputs)
        self.entry_category.grid(row=1, column=1)

        self.label_amount = tk.Label(self.frame_inputs, text="Összeg")
        self.label_amount.grid(row=2, column=0)
        self.entry_amount = tk.Entry(self.frame_inputs)
        self.entry_amount.grid(row=2, column=1)

        self.label_description = tk.Label(self.frame_inputs, text="Megjegyzés")
        self.label_description.grid(row=3, column=0)
        self.entry_description = tk.Entry(self.frame_inputs)
        self.entry_description.grid(row=3, column=1)

        self.button_add = tk.Button(self.frame_inputs, text="Hozzáadás", command=self.add_expense)
        self.button_add.grid(row=4, column=0, pady=5)

        self.button_delete = tk.Button(self.frame_inputs, text="Törlés", command=self.delete_selected)
        self.button_delete.grid(row=4, column=1, pady=5)

        self.frame_list = tk.Frame(self.root)
        self.frame_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.listbox_expenses = tk.Listbox(self.frame_list, width=60, height=10)
        self.listbox_expenses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_expenses = tk.Scrollbar(self.frame_list)
        self.scrollbar_expenses.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_expenses.config(yscrollcommand=self.scrollbar_expenses.set)
        self.scrollbar_expenses.config(command=self.listbox_expenses.yview)

        self.label_total = tk.Label(self.root, text="Összesen: 0")
        self.label_total.pack(padx=10, pady=(0, 10))

        self.load_from_file()

    def load_from_file(self):
        self.expenses = load_expenses_from_csv_bs(self.filename)
        self.listbox_expenses.delete(0, tk.END)
        for expense in self.expenses:
            line = f"{expense.date} | {expense.category} | {expense.amount} | {expense.description}"
            self.listbox_expenses.insert(tk.END, line)
        total = osszeg_bs(self.expenses)
        self.label_total.config(text=f"Összesen: {total}")

    def add_expense(self):
        date = self.entry_date.get()
        category = self.entry_category.get()
        amount_text = self.entry_amount.get()
        description = self.entry_description.get()

        if not amount_text:
            return

        try:
            amount = float(amount_text)
        except ValueError:
            return

        if not date:
            date = "ismeretlen"

        if not category:
            category = "egyéb"

        expense = ExpenseBS(date, category, amount, description)
        self.expenses.append(expense)

        line = f"{date} | {category} | {amount} | {description}"
        self.listbox_expenses.insert(tk.END, line)

        total = osszeg_bs(self.expenses)
        self.label_total.config(text=f"Összesen: {total}")

        save_expenses_to_csv_bs(self.expenses, self.filename)

        self.entry_date.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)

    def delete_selected(self):
        selection = self.listbox_expenses.curselection()
        if not selection:
            return
        index = selection[0]
        if index < 0 or index >= len(self.expenses):
            return

        del self.expenses[index]
        self.listbox_expenses.delete(index)

        total = osszeg_bs(self.expenses)
        self.label_total.config(text=f"Összesen: {total}")

        save_expenses_to_csv_bs(self.expenses, self.filename)

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = App(root)
    app.run()


if __name__ == "__main__":
    main()
