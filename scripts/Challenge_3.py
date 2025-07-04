import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Create database connection from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

CONN_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Function to load CSV files into DataFrames
def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path)
    logging.info(f"Loaded {len(df)} rows from {path}")
    return df

# Function to validate and clean numeric columns
def validate_and_clean_numeric_column(
    df: pd.DataFrame,
    column: str,
    min_value: float = 0.0,
    log_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Delete rows with invalid values in the specified column.
    """
    invalid_df = df[df[column] < min_value]
    if not invalid_df.empty:
        logging.warning(f"{len(invalid_df)} invalid rows found in '{column}' < {min_value}. Removing.")
        if log_path:
            invalid_df.to_csv(log_path, index=False)
            logging.info(f"Invalid records exported to: {log_path}")
    return df[df[column] >= min_value]

def validate_foreign_keys(orders_df: pd.DataFrame, products_df: pd.DataFrame):
    missing = set(orders_df["product_id"]) - set(products_df["product_id"])
    if missing:
        logging.warning(f"{len(missing)} product_id(s) in orders not found in products: {missing}")

def setup_database(engine):
    with engine.connect() as conn:
        # Create tables if they don't exist
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price NUMERIC CHECK (price >= 0)
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                product_id INTEGER REFERENCES products(product_id),
                quantity INTEGER CHECK (quantity > 0),
                created_date DATE
            )
        """))
        logging.info("Tables created and loaded successfully.")

def insert_data(engine, df: pd.DataFrame, table_name: str):
    df.to_sql(table_name, engine, if_exists="append", index=False, method="multi")
    logging.info(f"Inserted {len(df)} rows into '{table_name}'")

def main():
    logging.info("Connecting to DB")
    engine = create_engine(CONN_URL)

    # Leer y limpiar productos
    products_df = load_csv("data/products.csv").rename(columns={"id": "product_id"})
    products_df = validate_and_clean_numeric_column(
        products_df,
        column="price",
        min_value=0,
        log_path="outputs/invalid_products.csv"
    )

    # Leer y limpiar órdenes
    orders_df = load_csv("data/orders.csv").rename(columns={"id": "order_id"})
    orders_df = validate_and_clean_numeric_column(
        orders_df,
        column="quantity",
        min_value=1,
        log_path="outputs/invalid_orders.csv"
    )

    # Validar claves foráneas
    validate_foreign_keys(orders_df, products_df)

    # Crear tablas y cargar
    setup_database(engine)
    insert_data(engine, products_df, "products")
    insert_data(engine, orders_df, "orders")

    logging.info("Data loaded into DB successfully")

if __name__ == "__main__":
    main()
