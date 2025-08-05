import joblib
import pandas as pd
import mysql.connector
from tkinter import messagebox

def load_model():
    """Load the house price prediction model."""
    try:
        model = joblib.load("indian_house_price_model.pk1")
        print("Model loaded successfully!")
        return model
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load model.\n{e}")
        return None

def predict_price(input_features):
    """Predict house price and save it to the database."""
    model = load_model()
    if model is None:
        return None
    try:
        # Convert to DataFrame and ensure numeric values
        input_df = pd.DataFrame([input_features], columns=["area_type(1,2)", "location (Cityno.)", "size(1BHK-5BHK)",
                                                           "society(361000-461000)", "total_sqft", "bathroom", "balcony"])
        input_df = input_df.apply(pd.to_numeric, errors='coerce')  # Ensure all numeric

        # Get prediction
        predicted_price = float(model.predict(input_df)[0])

        # Ensure price is not negative
        predicted_price = max(0, predicted_price)  

        # Save to database
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="house_price_db", port=3307)
        cursor = conn.cursor()
        sql = "INSERT INTO price_predictor1 (area_type, location, size, society, total_sqft, bathroom, balcony, predicted_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (*input_features, predicted_price))
        conn.commit()
        cursor.close()
        conn.close()
        
        return predicted_price
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong.\n{e}")
        return None
