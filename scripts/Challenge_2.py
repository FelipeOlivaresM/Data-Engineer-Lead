# scripts/challenge_2 Get exchange rate and convert total price
# Felipe Olivares

import pandas as pd
import requests
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

API_URL = "https://api.freecurrencyapi.com/v1/latest"

# Get exchange rate from API
# Parameters: api_key, base currency (default BRL), target currency (default USD)
def get_exchange_rate(api_key: str, base: str = "BRL", target: str = "USD") -> float:
    params = {"apikey": api_key,"base_currency": base}
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        rate = data.get("data", {}).get(target)
        if rate is None:
            raise ValueError(f"Missing '{target}' in response: {data}")
        if not isinstance(rate, (float, int)):
            raise TypeError(f"Invalid exchange rate type: {type(rate)}")

        logging.info(f"Retrieved exchange rate {base} → {target}: {rate}")
        return rate

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid response structure: {e}")
        raise

# Load order data from CSV
def load_order_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path)
    logging.info(f"Loaded {len(df)} rows from {path}")
    return df

# Apply conversion to total price
# Adds two new columns: total_price_br (original) and total_price_us (converted)
def apply_conversion(df: pd.DataFrame, rate: int) -> pd.DataFrame:
    df["total_price_br"] = df["total_price"]
    df["total_price_us"] = df["total_price_br"] * rate
    return df.drop(columns=["total_price"])

# Export DataFrame to CSV
def export_csv(df: pd.DataFrame, output_path: str) -> None:
    df.to_csv(output_path, index=False)
    logging.info(f"Saved file: {output_path} with {len(df)} rows")


def main():
    api_key = os.getenv("CURRENCY_API_KEY")
    if not api_key:
        raise EnvironmentError("CURRENCY_API_KEY not set")

    input_path = "outputs/order_full_information.csv"
    output_path = "outputs/fixed_order_full_information.csv"

    df = load_order_data(input_path)
    rate = get_exchange_rate(api_key)
    logging.info(f"Rate: {rate}")
    df_converted = apply_conversion(df, rate)
    export_csv(df_converted, output_path)

if __name__ == "__main__":
    main()
