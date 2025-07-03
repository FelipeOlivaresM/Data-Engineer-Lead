# scripts/challenge_2.2 Calculate KPIs from orders and products
# Felipe Olivares

import pandas as pd
import os

# Define file paths
orders_path = os.path.join("outputs", "fixed_order_full_information.csv")
products_path = os.path.join("data", "products.csv")
output_path = os.path.join("outputs", "kpi_product_orders.csv")

# Load data
orders_df = pd.read_csv(orders_path)
products_df = pd.read_csv(products_path)

# KPI 1: Date with the most orders
max_order_date = (
    orders_df.groupby("order_created_date")
    .size()
    .idxmax()
)

# KPI 2: Most demanded product and total sales
product_demand = (
    orders_df.groupby("product_name")[["quantity", "total_price_us"]]
    .sum()
    .sort_values("quantity", ascending=False)
)

most_demanded_product = product_demand.index[0]
total_sales_usd = round(product_demand.iloc[0]["total_price_us"], 2)

# KPI 3: Top 3 most demanded categories
# Join with products dataframe to get product categories names
merged = orders_df.merge(products_df, left_on="product_name", right_on="name")

category_demand = (
    merged.groupby("category")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

top_3_categories = " > ".join(category_demand.head(3).index)

# Save KPIs to CSV
kpi_data = {
    "kpi_name": [
        "max_order_date",
        "most_demanded_product",
        "most_demanded_product_sales",
        "top_categories"
    ],
    "value": [
        max_order_date,
        most_demanded_product,
        total_sales_usd,
        top_3_categories
    ]
}

kpi_df = pd.DataFrame(kpi_data)
kpi_df.to_csv(output_path, index=False)

#print(" KPIs generated and saved succesfully on file 'kpi_product_orders.csv'")
