# scripts/challenge_2 Get exchange rate and convert total price
# Felipe Olivares

import pandas as pd
import requests
import os

# Config Variables
API_KEY = os.getenv("CURRENCY_API_KEY")  
BASE_URL = "https://api.freecurrencyapi.com/v1/latest"
BASE_CURRENCY = "BRL"
TARGET_CURRENCY = "USD"

# Load previous data from CSV
input_path = os.path.join("outputs", "order_full_information.csv")
df = pd.read_csv(input_path)

# Get exchange rate from API
params = {
    "apikey": API_KEY,
    "base_currency": BASE_CURRENCY
}

response = requests.get(BASE_URL, params=params)
data = response.json()

rate = data["data"].get(TARGET_CURRENCY)
# Check if the rate was found, if not, raise an error
if not rate:
    raise ValueError("Not found base Currency from BRL to USD")

# print(f" Get currency rate from {rate:.4f} BRL to USD")  

# Rename current column and calculate total_price_us
df["total_price_br"] = df["total_price"]
df["total_price_us"] = df["total_price_br"] * rate
df = df.drop(columns=["total_price"])  # Drop original column to keep order

# Save result
output_path = os.path.join("outputs", "fixed_order_full_information.csv")
df.to_csv(output_path, index=False)

#print(f" File generated with rate {rate:.4f}: fixed_order_full_information.csv")
