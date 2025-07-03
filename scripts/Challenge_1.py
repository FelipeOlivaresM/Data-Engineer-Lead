# scripts/challenge_1_merge_csv.py

import pandas as pd
import os

# Cargar archivos CSV
products_path = os.path.join("data", "products.csv")
orders_path = os.path.join("data", "orders.csv")

products_df = pd.read_csv(products_path)
orders_df = pd.read_csv(orders_path)

# Unir los archivos por product_id

merged_df = orders_df.merge(
    products_df,
    how="left",
    left_on="product_id",
    right_on="id",
    suffixes=('_order', '_product')
)

# Formatear fecha
merged_df["created_date"] = pd.to_datetime(merged_df["created_date"]).dt.date

# Calcular el precio total por orden
merged_df["total_price"] = merged_df["quantity"] * merged_df["price"]

# Renombrar y seleccionar columnas
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

# Exportar archivo
output_path = os.path.join("outputs", "order_full_information.csv")
final_df.to_csv(output_path, index=False)

print("✅ Archivo 'order_full_information.csv' generado correctamente.")