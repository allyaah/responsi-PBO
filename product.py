import tkinter as tk
from tkinter import ttk, messagebox

class ProductManager:
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

        # Frame for product form
        form_frame = tk.Frame(parent, bg="#E1F5FE")
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(form_frame, text="Nama Produk:", bg="#E1F5FE", font=("Lucida Fax", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_product = ttk.Entry(form_frame, font=("Lucida Fax", 10))
        self.name_product.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Harga Produk:", bg="#E1F5FE", font=("Lucida Fax", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.price_product = ttk.Entry(form_frame, font=("Lucida Fax", 10))
        self.price_product.grid(row=1, column=1, padx=5, pady=5)

        # Button frame for action buttons
        button_frame = tk.Frame(parent, bg="#E1F5FE")
        button_frame.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(button_frame, text="Tambah Produk", command=self.add_product).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Update Produk", command=self.update_product).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Hapus Produk", command=self.delete_product).grid(row=0, column=2, padx=10)

        # Product table
        self.tree_product = ttk.Treeview(parent, columns=("ID", "Name", "Price"), show="headings", height=10)
        self.tree_product.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.tree_product.heading("ID", text="ID")
        self.tree_product.column("ID", width=50, anchor="center")
        self.tree_product.heading("Name", text="Nama Produk")
        self.tree_product.column("Name", width=200)
        self.tree_product.heading("Price", text="Harga Produk")
        self.tree_product.column("Price", width=100)

        self.tree_product.bind("<Double-1>", self.on_tree_select)

        self.load_product()

    def add_product(self):
        name = self.name_product.get()
        price = self.price_product.get()
        if not name or not price:
            messagebox.showwarning("Input Error", "Name and Price must be filled")
            return
        if not name.isalpha():
            messagebox.showwarning("Input Error", "Name must be a valid string")
            return
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be a positive number")
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))
            return
        self.db.execute_query("INSERT INTO product (name_product, price_product) VALUES (%s, %s)", (name, price))
        self.load_product()
        self.clear_form()

    def load_product(self):
        for row in self.tree_product.get_children():
            self.tree_product.delete(row)
        products = self.db.fetch_all("SELECT * FROM product")
        for item in products:
            self.tree_product.insert("", "end", values=item)

    def update_product(self):
        selected_item = self.tree_product.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a product to update")
            return
        item = self.tree_product.item(selected_item)
        product_id = item['values'][0]

        # Get the current values from the form
        name = self.name_product.get()
        price = self.price_product.get()

        if not name or not price:
            messagebox.showwarning("Input Error", "Name and Price must be filled")
            return
        if not name.isalpha():
            messagebox.showwarning("Input Error", "Name must be a valid string")
            return
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be a positive number")
        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))
            return

        # Update the database
        self.db.execute_query("UPDATE product SET name_product = %s, price_product = %s WHERE id_product = %s", (name, price, product_id))
        self.load_product()
        self.clear_form()

    def delete_product(self):
        selected_item = self.tree_product.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a product to delete")
            return
        item = self.tree_product.item(selected_item)
        product_id = item['values'][0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
        if confirm:
            self.db.execute_query("DELETE FROM product WHERE id_product = %s", (product_id,))
            self.load_product()
            self.clear_form()

    def on_tree_select(self, event):
        selected_item = self.tree_product.selection()
        if not selected_item:
            return
        item = self.tree_product.item(selected_item)
        product_id, name, price = item['values']

        # Automatically fill the form with the selected product's data
        self.name_product.delete(0, tk.END)
        self.name_product.insert(0, name)

        self.price_product.delete(0, tk.END)
        self.price_product.insert(0, price)

    def clear_form(self):
        self.name_product.delete(0, tk.END)
        self.price_product.delete(0, tk.END)
