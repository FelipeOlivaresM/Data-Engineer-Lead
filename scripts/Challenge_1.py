# scripts/challenge_1 Merge CSV files and calculate total price
# Felipe Olivares


import pandas as pd
import os

# Load CSV files
products_path = os.path.join("data", "products.csv")
orders_path = os.path.join("data", "orders.csv")

products_df = pd.read_csv(products_path)
orders_df = pd.read_csv(orders_path)

# Join files by product_id

merged_df = orders_df.merge(
    products_df,
    how="left",
    left_on="product_id",
    right_on="id",
    suffixes=('_order', '_product')
)

# Format date column
merged_df["created_date"] = pd.to_datetime(merged_df["created_date"]).dt.date

# Calculate price by order quantity
merged_df["total_price"] = merged_df["quantity"] * merged_df["price"]

# Rename and select columns
final_df = merged_df[[
    "created_date",
    "id_order",
    "name",
    "quantity",
    "total_price"
]].rename(columns={
    "created_date": "order_created_date",
    "id_order": "order_id",
    "name": "product_name"
})

# Export datafram to CSV
output_path = os.path.join("outputs", "order_full_information.csv")
final_df.to_csv(output_path, index=False)

#print("File 'order_full_information.csv' generated  successfully")