import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class TransactionManager:
    def __init__(self, db):
        self.db = db

    def create_ui(self, parent):
        # Set up styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TLabel", background="#E1F5FE", font=("Lucida Fax", 10))
        style.configure("TButton", background="#E1F5FE", foreground="black", font=("Lucida Fax", 10))
        style.map("TButton", background=[("active", "#81D4FA")])
        style.configure("Treeview", font=("Lucida Fax", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Lucida Fax", 10, "bold"), background="#E1F5FE", foreground="black")

        # Frame for transaction form
        form_frame = tk.Frame(parent, bg="#E1F5FE")
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(form_frame, text="Nama Produk:", bg="#E1F5FE", font=("Lucida Fax", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.product_dropdown = ttk.Combobox(form_frame, state="readonly", font=("Lucida Fax", 10))
        self.product_dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Jumlah:", bg="#E1F5FE", font=("Lucida Fax", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.total_product = ttk.Entry(form_frame, font=("Lucida Fax", 10))
        self.total_product.grid(row=1, column=1, padx=5, pady=5)

        # Button frame for action buttons
        button_frame = tk.Frame(parent, bg="#E1F5FE")
        button_frame.grid(row=1, column=0, padx=10, pady=10) 

        ttk.Button(button_frame, text="Tambah Transaksi", command=self.add_transaction).grid(row=0, column=0, columnspan=2, pady=10)

        # Transaction table
        self.tree_transaction = ttk.Treeview(parent, columns=("ID", "Product", "Jumlah", "Price", "Date"), show="headings", height=10)
        self.tree_transaction.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.tree_transaction.heading("ID", text="ID")
        self.tree_transaction.column("ID", width=50, anchor="center")
        self.tree_transaction.heading("Product", text="Nama Produk")
        self.tree_transaction.column("Product", width=200)
        self.tree_transaction.heading("Jumlah", text="Jumlah")
        self.tree_transaction.column("Jumlah", width=100)
        self.tree_transaction.heading("Price", text="Total Harga")
        self.tree_transaction.column("Price", width=100)
        self.tree_transaction.heading("Date", text="Tanggal Transaksi")
        self.tree_transaction.column("Date", width=150)

        self.load_product_dropdown()
        self.load_transaction()

    def load_product_dropdown(self):
        products = self.db.fetch_all("SELECT id_product, name_product FROM product")
        self.product_dropdown['values'] = [f"{p[0]} - {p[1]}" for p in products]

    def add_transaction(self):
        product = self.product_dropdown.get()
        total = self.total_product.get()
        if not product or not total:
            messagebox.showwarning("Input Error", "Product and Total must be filled")
            return
        try:
            total = int(total)
        except ValueError:
            messagebox.showwarning("Input Error", "Total must be a number")
            return
        if total <= 0:
            messagebox.showwarning("Input Error", "Total must be greater than 0")
            return
        id_product = int(product.split(" - ")[0])
        price_product = self.db.fetch_all("SELECT price_product FROM product WHERE id_product = %s", (id_product,))[0][0]
        total_price = total * price_product
        self.db.execute_query(
            "INSERT INTO transaction (id_product, total_product, total_price, transaction_date) VALUES (%s, %s, %s, %s)",
            (id_product, total, total_price, date.today())
        )
        self.load_transaction()

    def load_transaction(self):
        for row in self.tree_transaction.get_children():
            self.tree_transaction.delete(row)
        transactions = self.db.fetch_all(
            """
            SELECT t.id_transaction, p.name_product, t.total_product, t.total_price, t.transaction_date
            FROM transaction t
            JOIN product p ON t.id_product = p.id_product
            """
        )
        for item in transactions:
            self.tree_transaction.insert("", "end", values=item)
