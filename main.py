import tkinter as tk
from tkinter import ttk
from expenses_bs import ExpenseBS, osszeg_bs, save_expenses_to_csv_bs, load_expenses_from_csv_bs


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Költségkövető")
        self.root.geometry("920x620")
        self.root.minsize(900, 580)

        self.expenses = []
        self.filename = "expenses_bs.csv"
        self.displayed_indices = []
        self.search_text = tk.StringVar()
        self.summary_mode = tk.StringVar(value="napi")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg_main = "#0f172a"
        bg_card = "#111827"
        fg_text = "#e5e7eb"
        fg_muted = "#9ca3af"
        accent = "#4f46e5"

        self.root.configure(bg=bg_main)
        style.configure("Main.TFrame", background=bg_main)
        style.configure("Card.TFrame", background=bg_card, relief="flat")
        style.configure("Title.TLabel", background=bg_main, foreground=fg_text, font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", background=bg_main, foreground=fg_muted, font=("Segoe UI", 10))
        style.configure("CardLabel.TLabel", background=bg_card, foreground=fg_text, font=("Segoe UI", 10))
        style.configure("CardMuted.TLabel", background=bg_card, foreground=fg_muted, font=("Segoe UI", 9))
        style.configure("Card.TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Accent.TButton", background=accent, foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#6366f1")])
        style.configure("TEntry", padding=4)
        style.configure("Search.TEntry", padding=4)
        style.configure("Total.TLabel", background=bg_main, foreground=fg_text, font=("Segoe UI", 11, "bold"))
        style.configure("Summary.TLabel", background=bg_card, foreground=fg_text, font=("Segoe UI", 10, "bold"))

        style.configure("Treeview",
                        background="#020617",
                        foreground=fg_text,
                        fieldbackground="#020617",
                        rowheight=24,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background="#111827",
                        foreground=fg_muted,
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview",
                  background=[("selected", "#1d4ed8")],
                  foreground=[("selected", "#f9fafb")])

        self.frame_main = ttk.Frame(self.root, style="Main.TFrame")
        self.frame_main.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        self.frame_header = ttk.Frame(self.frame_main, style="Main.TFrame")
        self.frame_header.pack(fill=tk.X)

        self.label_title = ttk.Label(self.frame_header, text="Költségkövető", style="Title.TLabel")
        self.label_title.pack(anchor="w")

        self.label_subtitle = ttk.Label(
            self.frame_header,
            text="Mindennapi kiadások rögzítése, keresése és összesítése",
            style="Subtitle.TLabel"
        )
        self.label_subtitle.pack(anchor="w", pady=(2, 10))

        self.frame_top = ttk.Frame(self.frame_main, style="Main.TFrame")
        self.frame_top.pack(fill=tk.X)

        self.frame_inputs = ttk.Frame(self.frame_top, style="Card.TFrame")
        self.frame_inputs.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.label_inputs_title = ttk.Label(self.frame_inputs, text="Új tétel", style="Summary.TLabel")
        self.label_inputs_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 8), padx=12)

        self.label_date = ttk.Label(self.frame_inputs, text="Dátum", style="CardLabel.TLabel")
        self.label_date.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 3))
        self.entry_date = ttk.Entry(self.frame_inputs, width=18)
        self.entry_date.grid(row=1, column=1, sticky="ew", padx=12, pady=(0, 3))

        self.label_category = ttk.Label(self.frame_inputs, text="Kategória", style="CardLabel.TLabel")
        self.label_category.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 3))
        self.entry_category = ttk.Entry(self.frame_inputs, width=18)
        self.entry_category.grid(row=2, column=1, sticky="ew", padx=12, pady=(0, 3))

        self.label_amount = ttk.Label(self.frame_inputs, text="Összeg", style="CardLabel.TLabel")
        self.label_amount.grid(row=3, column=0, sticky="w", padx=12, pady=(0, 3))
        self.entry_amount = ttk.Entry(self.frame_inputs, width=18)
        self.entry_amount.grid(row=3, column=1, sticky="ew", padx=12, pady=(0, 3))

        self.label_description = ttk.Label(self.frame_inputs, text="Megjegyzés", style="CardLabel.TLabel")
        self.label_description.grid(row=4, column=0, sticky="w", padx=12, pady=(0, 3))
        self.entry_description = ttk.Entry(self.frame_inputs, width=18)
        self.entry_description.grid(row=4, column=1, sticky="ew", padx=12, pady=(0, 10))

        self.button_add = ttk.Button(self.frame_inputs, text="Hozzáadás", style="Accent.TButton",
                                     command=self.add_expense)
        self.button_delete = ttk.Button(self.frame_inputs, text="Törlés", style="Card.TButton",
                                        command=self.delete_selected)

        self.button_add.grid(row=5, column=0, padx=12, pady=(0, 12), sticky="ew")
        self.button_delete.grid(row=5, column=1, padx=12, pady=(0, 12), sticky="ew")

        self.frame_inputs.columnconfigure(0, weight=1)
        self.frame_inputs.columnconfigure(1, weight=1)

        self.frame_summary_card = ttk.Frame(self.frame_top, style="Card.TFrame")
        self.frame_summary_card.grid(row=0, column=1, sticky="nsew")

        self.label_summary_title = ttk.Label(self.frame_summary_card, text="Összesítések", style="Summary.TLabel")
        self.label_summary_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 4), padx=12)

        self.radio_daily = ttk.Radiobutton(
            self.frame_summary_card,
            text="Napi összesítés",
            variable=self.summary_mode,
            value="napi"
        )
        self.radio_daily.grid(row=1, column=0, sticky="w", padx=12, pady=(4, 0))

        self.radio_monthly = ttk.Radiobutton(
            self.frame_summary_card,
            text="Havi összesítés",
            variable=self.summary_mode,
            value="havi"
        )
        self.radio_monthly.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(4, 0))

        self.label_summary_date = ttk.Label(self.frame_summary_card, text="Dátum / hónap", style="CardLabel.TLabel")
        self.label_summary_date.grid(row=2, column=0, sticky="w", padx=12, pady=(10, 3))

        self.entry_summary_date = ttk.Entry(self.frame_summary_card)
        self.entry_summary_date.grid(row=2, column=1, sticky="ew", padx=(0, 12), pady=(10, 3))

        self.button_summary = ttk.Button(self.frame_summary_card, text="Számítás", style="Card.TButton",
                                         command=self.calculate_summary)
        self.button_summary.grid(row=2, column=2, sticky="ew", padx=(0, 12), pady=(10, 3))

        self.label_summary = ttk.Label(self.frame_summary_card, text="Összesítés: 0", style="CardLabel.TLabel")
        self.label_summary.grid(row=3, column=0, columnspan=3, sticky="w", padx=12, pady=(8, 12))

        self.frame_summary_card.columnconfigure(1, weight=1)

        self.frame_top.columnconfigure(0, weight=1)
        self.frame_top.columnconfigure(1, weight=1)

        self.frame_search = ttk.Frame(self.frame_main, style="Main.TFrame")
        self.frame_search.pack(fill=tk.X, pady=(14, 6))

        self.label_search = ttk.Label(self.frame_search, text="Keresés", style="Subtitle.TLabel")
        self.label_search.pack(side=tk.LEFT, padx=(2, 6))

        self.entry_search = ttk.Entry(self.frame_search, textvariable=self.search_text, style="Search.TEntry")
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.button_search = ttk.Button(self.frame_search, text="Szűrés", style="Card.TButton",
                                        command=self.apply_search)
        self.button_search.pack(side=tk.LEFT, padx=(8, 4))

        self.button_clear_search = ttk.Button(self.frame_search, text="Szűrés törlése", style="Card.TButton",
                                              command=self.clear_search)
        self.button_clear_search.pack(side=tk.LEFT)

        self.frame_list = ttk.Frame(self.frame_main, style="Main.TFrame")
        self.frame_list.pack(fill=tk.BOTH, expand=True)

        self.tree_expenses = ttk.Treeview(
            self.frame_list,
            columns=("date", "category", "amount", "description"),
            show="headings",
            selectmode="browse",
            height=12
        )
        self.tree_expenses.heading("date", text="Dátum")
        self.tree_expenses.heading("category", text="Kategória")
        self.tree_expenses.heading("amount", text="Összeg")
        self.tree_expenses.heading("description", text="Megjegyzés")

        self.tree_expenses.column("date", width=110, anchor="w")
        self.tree_expenses.column("category", width=150, anchor="w")
        self.tree_expenses.column("amount", width=90, anchor="w")
        self.tree_expenses.column("description", width=320, anchor="w")

        self.tree_expenses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_expenses = ttk.Scrollbar(self.frame_list, orient=tk.VERTICAL,
                                                command=self.tree_expenses.yview)
        self.scrollbar_expenses.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_expenses.configure(yscrollcommand=self.scrollbar_expenses.set)

        self.frame_bottom = ttk.Frame(self.frame_main, style="Main.TFrame")
        self.frame_bottom.pack(fill=tk.X, pady=(8, 0))

        self.label_total = ttk.Label(self.frame_bottom, text="Összesen: 0", style="Total.TLabel")
        self.label_total.pack(anchor="e")

        self.load_from_file()

    def load_from_file(self):
        self.expenses = load_expenses_from_csv_bs(self.filename)
        self.refresh_list()
        self.update_total()
        self.label_summary.config(text="Összesítés: 0")

    def refresh_list(self):
        for item in self.tree_expenses.get_children():
            self.tree_expenses.delete(item)
        self.displayed_indices = []
        filter_text = self.search_text.get().strip().lower()
        for index, expense in enumerate(self.expenses):
            line = f"{expense.date} | {expense.category} | {expense.amount} | {expense.description}"
            if filter_text and filter_text not in line.lower():
                continue
            self.displayed_indices.append(index)
            self.tree_expenses.insert(
                "",
                tk.END,
                values=(expense.date, expense.category, expense.amount, expense.description)
            )

    def update_total(self):
        total = osszeg_bs(self.expenses)
        self.label_total.config(text=f"Összesen: {total}")

    def apply_search(self):
        self.refresh_list()

    def clear_search(self):
        self.search_text.set("")
        self.refresh_list()

    def add_expense(self):
        date = self.entry_date.get()
        category = self.entry_category.get()
        amount_text = self.entry_amount.get()
        description = self.entry_description.get()

        if not amount_text:
            return

        try:
            amount = int(amount_text)
        except ValueError:
            return

        if not date:
            date = "ismeretlen"

        if not category:
            category = "egyéb"

        expense = ExpenseBS(date, category, amount, description)
        self.expenses.append(expense)

        save_expenses_to_csv_bs(self.expenses, self.filename)

        self.refresh_list()
        self.update_total()
        self.label_summary.config(text="Összesítés: 0")

        self.entry_date.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)

    def delete_selected(self):
        selection = self.tree_expenses.selection()
        if not selection:
            return
        item_id = selection[0]
        children = list(self.tree_expenses.get_children())
        if item_id not in children:
            return
        visible_index = children.index(item_id)
        if visible_index < 0 or visible_index >= len(self.displayed_indices):
            return
        expense_index = self.displayed_indices[visible_index]

        del self.expenses[expense_index]
        save_expenses_to_csv_bs(self.expenses, self.filename)

        self.refresh_list()
        self.update_total()
        self.label_summary.config(text="Összesítés: 0")

    def calculate_summary(self):
        mode = self.summary_mode.get()
        date_text = self.entry_summary_date.get().strip()
        if not date_text:
            self.label_summary.config(text="Összesítés: 0")
            return
        total = 0
        if mode == "napi":
            for expense in self.expenses:
                if expense.date.strip() == date_text:
                    total += expense.amount
        else:
            for expense in self.expenses:
                if expense.date.startswith(date_text):
                    total += expense.amount
        self.label_summary.config(text=f"Összesítés: {total}")

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = App(root)
    app.run()


if __name__ == "__main__":
    main()
