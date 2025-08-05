import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import subprocess

# Function to connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="house_price_db",
            port=3307
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to fetch data from a table
def fetch_data(table_name):
    conn = connect_db()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []
    finally:
        conn.close()

# Function to update a record
def update_record(table, tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No record selected!")
        return
    
    values = tree.item(selected_item, "values")
    if not values:
        return

    # Create Update Window
    update_win = tk.Toplevel()
    update_win.title("Update Record")
    update_win.geometry("400x300")

    fields = tree["columns"]
    entries = {}

    for i, field in enumerate(fields):
        tk.Label(update_win, text=field).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(update_win)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, values[i])
        entries[field] = entry

    def save_update():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            update_query = f"UPDATE {table} SET " + ", ".join([f"{field}=%s" for field in fields[1:]]) + " WHERE id=%s"
            values_to_update = [entries[field].get() for field in fields[1:]] + [values[0]]
            cursor.execute(update_query, values_to_update)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record updated successfully!")
            update_win.destroy()
            load_data()

    tk.Button(update_win, text="Update", command=save_update).grid(row=len(fields), column=0, columnspan=2, pady=10)

# Function to delete a record
def delete_record(table, tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No record selected!")
        return
    
    values = tree.item(selected_item, "values")
    if not values:
        return

    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this record?")
    if confirm:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id=%s", (values[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record deleted successfully!")
            load_data()

# Function to load data into the table
def load_data():
    for tree in [tree_price, tree_users]:
        tree.delete(*tree.get_children())  

    data_price = fetch_data("price_predictor1")
    for row in data_price:
        tree_price.insert("", "end", values=row)

    data_users = fetch_data("users")
    for row in data_users:
        tree_users.insert("", "end", values=row)

# Function to open the login page
def back_to_login():
    root.destroy()
    subprocess.run(["python", "login.py"])

# Function to create the Admin Dashboard window
def open_admin_dashboard():
    global tree_price, tree_users, root

    root = tk.Tk()
    root.title("Admin Dashboard")
    root.attributes('-fullscreen', True)

    # Frame for price predictor table
    frame1 = tk.LabelFrame(root, text="House Price Data", font=("Arial", 12, "bold"), padx=10, pady=10)
    frame1.pack(expand=True, fill="both", padx=10, pady=10)

    tree_price = ttk.Treeview(frame1, columns=("id", "location", "area_type", "size", "society", "total_sqft", "bathroom", "balcony", "predicted_price"), show="headings")
    for col in tree_price["columns"]:
        tree_price.heading(col, text=col)
        tree_price.column(col, width=100, anchor="center")
    tree_price.pack(expand=True, fill="both")

    # Buttons for house price table
    btn_frame1 = tk.Frame(frame1)
    btn_frame1.pack(pady=5)
    tk.Button(btn_frame1, text="Update", command=lambda: update_record("price_predictor1", tree_price), bg="lightblue", width=15).pack(side="left", padx=5)
    tk.Button(btn_frame1, text="Delete", command=lambda: delete_record("price_predictor1", tree_price), bg="red", fg="white", width=15).pack(side="left", padx=5)

    # Frame for users table
    frame2 = tk.LabelFrame(root, text="Users", font=("Arial", 12, "bold"), padx=10, pady=10)
    frame2.pack(expand=True, fill="both", padx=10, pady=10)

    tree_users = ttk.Treeview(frame2, columns=("id", "username", "password", "role"), show="headings")
    for col in tree_users["columns"]:
        tree_users.heading(col, text=col)
        tree_users.column(col, width=100, anchor="center")
    tree_users.pack(expand=True, fill="both")

    # Buttons for users table
    btn_frame2 = tk.Frame(frame2)
    btn_frame2.pack(pady=5)
    tk.Button(btn_frame2, text="Update", command=lambda: update_record("users", tree_users), bg="lightblue", width=15).pack(side="left", padx=5)
    tk.Button(btn_frame2, text="Delete", command=lambda: delete_record("users", tree_users), bg="red", fg="white", width=15).pack(side="left", padx=5)

    # Buttons for refresh, back, and exit
    tk.Button(root, text="Refresh Data", command=load_data, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(root, text="Back to Login", command=back_to_login, bg="red", fg="black", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy, bg="gray", font=("Arial", 12, "bold")).pack(pady=10)

    load_data()
    root.mainloop()

# Uncomment this to run directly
# open_admin_dashboard()
