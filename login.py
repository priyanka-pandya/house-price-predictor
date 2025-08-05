import tkinter as tk
from tkinter import messagebox
import mysql.connector
import admin_dashboard
import user_dashboard
import subprocess  
from PIL import Image, ImageTk

# Load background image BEFORE creating root window
image_path = r"C:/Users/WELCOME/Desktop/Pricing Predictor/img/loginpic.png" 

try:
    img = Image.open(image_path)  
    img = img.resize((1200, 700))  
    bg_photo = None  # Initialize it before using
except Exception as e:
    print(f"Error loading image: {e}")
    bg_photo = None  

# Tkinter Login GUI
root = tk.Tk()
root.title("Login")
root.attributes('-fullscreen', True)  

# Convert image after Tkinter window is created
if bg_photo is None:
    try:
        bg_photo = ImageTk.PhotoImage(img)  
    except Exception as e:
        print(f"Error processing image: {e}")

# Set Background (Only if image loaded successfully)
if bg_photo:
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    root.bg_image = bg_photo  

# Login Frame (Restored Styling)
frame = tk.Frame(root, bg="white", bd=5)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Username:", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(frame, font=("Arial", 14))
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Password:", font=("Arial", 14, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(frame, font=("Arial", 14), show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Login Button
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="house_price_db", port=3307)
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    
    conn.close()

    if result:
        role = result[0]
        root.destroy()  

        if role == 'admin':
            admin_dashboard.open_admin_dashboard()  
        else:
            user_dashboard.open_user_dashboard()  
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

login_button = tk.Button(frame, text="Login", font=("Arial", 12, "bold"), bg="lightblue", width=15, command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Function to open register window
def open_register():
    root.destroy()  
    subprocess.run(["python", "register.py"])  

# Register Button
register_button = tk.Button(frame, text="Register", font=("Arial", 12, "bold"), bg="lightgreen", width=15, command=open_register)
register_button.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
