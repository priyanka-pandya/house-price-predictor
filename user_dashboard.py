import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from house_price import predict_price  # Import prediction function
import subprocess  # To open the login.py file

def open_user_dashboard():
    root = tk.Tk()
    root.title("INDIAN HOUSE PRICE PREDICTOR")
    root.attributes('-fullscreen', True)

    # Load background image
    try:
        bg_image = Image.open(r"C:\Users\WELCOME\Desktop\Pricing Predictor\img\house.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Full-screen fix
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image.\n{e}")

    # Make window slightly transparent
    root.attributes('-alpha', 0.98)

    labels = ["Area Type (1,2)", "Location (City no.)", "Size (1BHK-5BHK)", "Society (361000-461000)", 
              "Total Sqft", "Bathroom", "Balcony"]
    entries = []

    # Lowering the input fields further down
    start_y = 0.45  # Moved down from 0.3
    spacing = 0.06  # Increased spacing for better layout

    for i, label in enumerate(labels):
        tk.Label(root, text=label, font=("Arial", 14, "bold"), bg="#2E3B55", fg="white").place(relx=0.4, rely=start_y + i*spacing, anchor="e")
        entry = tk.Entry(root, font=("Arial", 12), bg="white")
        entry.place(relx=0.42, rely=start_y + i*spacing, relwidth=0.15, anchor="w")
        entries.append(entry)

    def handle_prediction():
        try:
            input_values = [float(entry.get()) for entry in entries]
            predicted_price = predict_price(input_values)
            if predicted_price is not None:
                messagebox.showinfo("Prediction", f"Estimated House Price: Rs {predicted_price:,.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter numbers only.")

    # Predict Button
    tk.Button(root, text="Predict Price", font=("Arial", 12), bg="lightblue", command=handle_prediction).place(relx=0.42, rely=0.90, anchor="center")

    # Back to Login Button
    def back_to_login():
        root.destroy()  # Close current window
        subprocess.run(["python", "login.py"])  # Open login.py

    tk.Button(root, text="Back to Login", font=("Arial", 12), bg="red", fg="white", command=back_to_login).place(relx=0.52, rely=0.95, anchor="center")

    # Log Out Button
    tk.Button(root, text="Log Out", font=("Arial", 12), bg="red", fg="white", command=root.destroy).place(relx=0.42, rely=0.95, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    open_user_dashboard()
