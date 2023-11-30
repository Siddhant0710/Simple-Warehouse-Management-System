import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import ttk, font, messagebox
import mysql.connector
class WarehouseManagementApp:
    def create_ui(self):
        self.root.title("Warehouse Management System")
        self.root.geometry("700x600")

        # Add a Product Button
        add_product_btn = tk.Button(self.root, text="Add a Product", bg='LightBlue1', fg='black', width=20, height=2, command=self.show_add_product_dialog)
        add_product_btn['font'] = font.Font(size=12)
        add_product_btn.place(x=270, y=175)

        # Delete a Product Button
        delete_product_btn = tk.Button(self.root, text="Delete a Product", bg='misty rose', fg='black', width=20, height=2, command=self.delete_product)
        delete_product_btn['font'] = font.Font(size=12)
        delete_product_btn.place(x=270, y=255)

        # View Products Button
        view_products_btn = tk.Button(self.root, text="View Products", bg='old lace', fg='black', width=20, height=2, command=self.view_products)
        view_products_btn['font'] = font.Font(size=12)
        view_products_btn.place(x=270, y=335)

        # New Customer Button
        new_customer_btn = tk.Button(self.root, text="New Customer", bg='lavender blush2', fg='black', width=20, height=2, command=self.new_customer)
        new_customer_btn['font'] = font.Font(size=12)
        new_customer_btn.place(x=270, y=415)

    def show_add_product_dialog(self):
        # Create a new dialog window for adding a product
        add_product_window = tk.Toplevel(self.root)
        add_product_window.title("Add Product")
        add_product_window.geometry("400x200")

        tk.Label(add_product_window, text="Product Name:", font=font.Font(size=12, weight="bold")).pack()
        self.prod_name = tk.Entry(add_product_window)
        self.prod_name.pack()

        tk.Label(add_product_window, text="Product Price:", font=font.Font(size=12, weight="bold")).pack()
        self.prod_price = tk.Entry(add_product_window)
        self.prod_price.pack()

        tk.Label(add_product_window, text="Date:", font=font.Font(size=12, weight="bold")).pack()
        self.prod_date = tk.Entry(add_product_window)
        self.prod_date.pack()

        add_button = tk.Button(add_product_window, text="Add", bg='LightBlue1', fg='black', width=10, height=1, command=self.add_product)
        add_button['font'] = font.Font(size=12)
        add_button.pack()

    def get_product_details_for_deletion(self):
        product_name = simpledialog.askstring("Product Deletion", "Enter Product Name:")
        product_price = simpledialog.askfloat("Product Deletion", "Enter Product Price:")
        
        return product_name, product_price

    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Management System")
        self.root.geometry("700x600")
        
        self.init_db()
        self.create_ui()

    def init_db(self):
        self.db = mysql.connector.connect(
            user="root",
            passwd="siddhant",
            host="localhost",
            database="shop"
        )
        self.cursor = self.db.cursor()
        self.create_tables()

    def create_tables(self):
        # Create the 'shop' database if it doesn't exist
        create_database_query = "CREATE DATABASE IF NOT EXISTS shop"
        self.cursor.execute(create_database_query)

        # Use the 'shop' database
        self.cursor.execute("USE shop")
        create_products_table = """
            CREATE TABLE IF NOT EXISTS products (
                date DATE,
                prodName VARCHAR(50),
                prodPrice DECIMAL(10, 2)
            )
        """
        self.cursor.execute(create_products_table)
        self.db.commit()

        create_sale_table = """
            CREATE TABLE IF NOT EXISTS sale (
                custName VARCHAR(50),
                date DATE,
                prodName VARCHAR(50),
                qty INT,
                price DECIMAL(10, 2)
            )
        """
        self.cursor.execute(create_sale_table)
        self.db.commit()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def add_product(self):
        pname = self.prod_name.get()
        price = self.prod_price.get()
        date = self.prod_date.get()

        try:
            query = "INSERT INTO products (date, prodName, prodPrice) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (date, pname, price))
            self.db.commit()
            self.show_message("Success", "Product added successfully")
        except Exception as e:
            self.show_message("Error", f"Error adding data to the database: {e}")

    def delete_product(self):
        self.show_delete_product_dialog()

    def show_delete_product_dialog(self):
        # Create a new dialog window for deleting a product
        delete_product_window = tk.Toplevel(self.root)
        delete_product_window.title("Delete Product")
        delete_product_window.geometry("400x200")

        tk.Label(delete_product_window, text="Product Name:", font=font.Font(size=12, weight="bold")).pack()
        self.delete_prod_name = tk.Entry(delete_product_window)
        self.delete_prod_name.pack()

        tk.Label(delete_product_window, text="Product Price:", font=font.Font(size=12, weight="bold")).pack()
        self.delete_prod_price = tk.Entry(delete_product_window)
        self.delete_prod_price.pack()

        delete_button = tk.Button(delete_product_window, text="Delete", bg='misty rose', fg='black', width=10, height=1, command=self.validate_and_delete_product)
        delete_button['font'] = font.Font(size=12)
        delete_button.pack()

    def validate_and_delete_product(self):
        product_name = self.delete_prod_name.get()
        product_price = self.delete_prod_price.get()

        if not product_name or not product_price:
            self.show_message("Error", "Please enter both product name and price.")
        else:
            try:
                query = "DELETE FROM products WHERE LOWER(prodName) = %s AND prodPrice = %s"
                self.cursor.execute(query, (product_name.lower(), product_price))
                self.db.commit()
                self.show_message("Success", "Product removed successfully")
            except Exception as e:
                self.show_message("Error", f"Error deleting data from the database: {e}")

    def view_products(self):
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("View Products")
        self.view_window.geometry("1000x400")

        products_tree = ttk.Treeview(self.view_window, columns=("Date", "Product Name", "Product Price"))
        products_tree.heading("#1", text="Date")
        products_tree.heading("#2", text="Product Name")
        products_tree.heading("#3", text="Product Price")
        products_tree.pack()

        try:
            query = "SELECT * FROM products"
            self.cursor.execute(query)
            products = self.cursor.fetchall()

            for product in products:
                products_tree.insert("", "end", values=product)

        except Exception as e:
            self.show_message("Error", f"Error fetching data from the database: {e}")

    def generate_bill(self):
        cust_name = self.cust_name.get()
        date = self.bill_date.get()
        total_bill = 0

        try:
            query = "SELECT * FROM sale WHERE custName = %s AND date = %s"
            self.cursor.execute(query, (cust_name, date))
            sale_data = self.cursor.fetchall()

            bill_window = tk.Toplevel(self.root)
            bill_window.title("Bill")
            bill_window.geometry("600x400")

            bill_tree = ttk.Treeview(bill_window, columns=("Product Name", "Price", "Quantity", "Total"))
            bill_tree.heading("#1", text="Product Name")
            bill_tree.heading("#2", text="Price")
            bill_tree.heading("#3", text="Quantity")
            bill_tree.heading("#4", text="Total")
            bill_tree.pack()

            for row in sale_data:
                product_name, _, _, qty, price = row
                total = qty * price
                bill_tree.insert("", "end", values=(product_name, price, qty, total))
                total_bill += total

            tk.Label(bill_window, text="Total Bill:", font=font.Font(size=12, weight="bold")).pack()
            tk.Label(bill_window, text=f"${total_bill:.2f}", font=font.Font(size=12, weight="bold")).pack()

        except Exception as e:
            self.show_message("Error", f"Error generating bill: {e}")

    def new_customer(self):
        self.new_customer_window = tk.Toplevel(self.root)
        self.new_customer_window.title("New Customer")
        self.new_customer_window.geometry("400x300")

        tk.Label(self.new_customer_window, text="Customer Name:", font=font.Font(size=12, weight="bold")).pack()
        self.cust_name = tk.Entry(self.new_customer_window)
        self.cust_name.pack()

        tk.Label(self.new_customer_window, text="Date:", font=font.Font(size=12, weight="bold")).pack()
        self.bill_date = tk.Entry(self.new_customer_window)
        self.bill_date.pack()

        tk.Button(self.new_customer_window, text="Generate Bill", font=font.Font(size=12),
        command=self.generate_bill).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseManagementApp(root)
    root.mainloop()