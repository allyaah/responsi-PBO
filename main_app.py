import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from product import ProductManager
from transaction import TransactionManager
from db import Database

class App:
    def __init__(self, root):
        self.db = Database()
        self.product_manager = ProductManager(self.db)
        self.transaction_manager = TransactionManager(self.db)

        self.root = root
        self.root.title("Manajemen Produk dan Transaksi")
        self.root.geometry("800x600")
        self.root.configure(bg="#BBDEFB")  # Set the background color to light blue

        # Set up styles to match the second file
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TLabel", background="#BBDEFB", font=("Lucida Fax", 10))
        style.configure("TButton", background="#BBDEFB", foreground="black", font=("Lucida Fax", 10))
        style.map("TButton", background=[("active", "#81D4FA")])
        style.configure("Treeview", font=("Lucida Fax", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Lucida Fax", 10, "bold"), background="#BBDEFB", foreground="black")

        self.create_widgets()

    def create_widgets(self):
        # Tab Control
        style = ttk.Style()

        # Style the Notebook (tab container)
        style.configure("TNotebook", background="#BBDEFB")
        style.configure("TNotebook.Tab", background="#BBDEFB", font=("Lucida Fax", 10), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#81D4FA")], foreground=[("selected", "black")])

        self.tab_control = ttk.Notebook(self.root, style="TNotebook")
        self.tab_produk = ttk.Frame(self.tab_control, style="TFrame")
        self.tab_transaksi = ttk.Frame(self.tab_control, style="TFrame")

        self.tab_control.add(self.tab_produk, text="Manajemen Produk")
        self.tab_control.add(self.tab_transaksi, text="Transaksi")
        self.tab_control.pack(expand=1, fill="both", pady=10)

        self.create_produk_tab()
        self.create_transaksi_tab()


    def create_produk_tab(self):
        # Creating the product management UI
        self.product_manager.create_ui(self.tab_produk)

    def create_transaksi_tab(self):
        # Creating the transaction management UI
        self.transaction_manager.create_ui(self.tab_transaksi)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
