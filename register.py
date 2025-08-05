import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import subprocess  # Required to go back to login

# Function to submit registration
def submit_registration():
    username = entry_user.get()
    password = entry_pass.get()
    role = role_var.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="house_price_db", port=3307)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        reg_window.destroy()
        subprocess.run(["python", "login.py"])  # Go back to login
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to go back to login
def go_back():
    reg_window.destroy()
    subprocess.run(["python", "login.py"])  # Open login.py

# Tkinter Register GUI
reg_window = tk.Tk()
reg_window.title("Register")
reg_window.attributes('-fullscreen', True)  # Full-screen mode

# Load and resize background image
image_path = r"C:/Users/WELCOME/Desktop/Pricing Predictor/img/loginpic.png"  # Ensure path is correct
try:
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((1200, 700))  # Resize to match login.py
    bg_image = ImageTk.PhotoImage(bg_image)
except Exception as e:
    print(f"Error loading image: {e}")
    bg_image = None

if bg_image:
    bg_label = tk.Label(reg_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    reg_window.bg_image = bg_image  # Prevent Garbage Collection

# Registration Frame
frame = tk.Frame(reg_window, bg="white", bd=5)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Username:", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
entry_user = tk.Entry(frame, font=("Arial", 14))
entry_user.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Password:", font=("Arial", 14, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5)
entry_pass = tk.Entry(frame, show="*", font=("Arial", 14))
entry_pass.grid(row=1, column=1, padx=10, pady=5)

# Role Selection
tk.Label(frame, text="Role:", font=("Arial", 14, "bold"), bg="white").grid(row=2, column=0, padx=10, pady=5)
role_var = tk.StringVar(value="user")
tk.Radiobutton(frame, text="User", variable=role_var, value="user", bg="white", font=("Arial", 12)).grid(row=2, column=1, sticky="w")
tk.Radiobutton(frame, text="Admin", variable=role_var, value="admin", bg="white", font=("Arial", 12)).grid(row=3, column=1, sticky="w")

# Register Button
tk.Button(frame, text="Register", font=("Arial", 12, "bold"), bg="lightgreen", width=15, command=submit_registration).grid(row=4, column=0, columnspan=2, pady=10)

# Back to Login Button
tk.Button(frame, text="Back to Login", font=("Arial", 12, "bold"), bg="red", width=15, command=go_back).grid(row=5, column=0, columnspan=2, pady=5)

reg_window.mainloop()
