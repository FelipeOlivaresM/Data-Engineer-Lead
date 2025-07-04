# scripts/challenge_3_postgres_loader.py
# Felipe Olivares

import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

conn_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conn_url)

# Cargar CSVs
products_df = pd.read_csv("data/products.csv")
orders_df = pd.read_csv("data/orders.csv")

# Rename columns to avoid name conflicts
products_df = products_df.rename(columns={"id": "product_id"})
orders_df = orders_df.rename(columns={"id": "order_id"})

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS orders"))
    conn.execute(text("DROP TABLE IF EXISTS products"))

    conn.execute(text("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price NUMERIC
        )
    """))

    conn.execute(text("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER,
            created_date DATE
        )
    """))

# Load data into PostgreSQL
products_df.to_sql("products", engine, if_exists="append", index=False)
orders_df.to_sql("orders", engine, if_exists="append", index=False)

# print("Data loaded into PostgreSQL successfully")
