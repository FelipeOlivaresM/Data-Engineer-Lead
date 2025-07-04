# 🧠 Lead Data Engineer Technical Assessment (English Version)

This repository contains the complete solution for the Lead Data Engineer technical assessment. It includes data processing, API integration, PostgreSQL loading, analytical queries, performance strategies, and architectural proposals.


Data-Engineer-Lead/
│
├── data/                   # Original CSV files
│   ├── orders.csv
│   └── products.csv
│
├── outputs/                # Generated outputs
│   ├── order_full_information.csv
│   ├── fixed_order_full_information.csv
│   └── kpi_product_orders.csv
│
├── scripts/                # Python and SQL scripts
│   ├── challenge_1_merge_csv.py
│   ├── challenge_2_currency_conversion.py
│   ├── challenge_2_kpi_analysis.py
│   ├── challenge_3_postgres_loader.py
│   ├── challenge_3_create_indexes.sql
│   ├── challenge_3_kpi_queries.sql
│   └── challenge_4_proposal.md
│
├── .env                    # Environment variables (excluded from Git)
├── .gitignore
├── requirements.txt
└── README.md               # This file



🧐 Challenge 1: Merging Orders and Products Data

✅ Goal:

Merge orders.csv and products.csv to generate order_full_information.csv with:

order_created_date

order_id

product_name

quantity

total_price (calculated as price * quantity)

🛠️ Tools:

Python

pandas

📃 Implementation:

Load both CSVs

Merge on product_id

Calculate total price

Format columns and export CSV

✨ Improvements:

Validate missing or orphan product_id

Use type hints and logging for production readiness

🌟 Challenge 2: Currency Conversion and KPIs

✅ Part A: BRL to USD Conversion

API: freecurrencyapi.com

API key loaded via .env

Generated fixed_order_full_information.csv with:

total_price_br

total_price_us (using real-time rate)

✅ Part B: KPIs Generation

Produced kpi_product_orders.csv with:

Date with the highest number of orders

Most demanded product + total sales in USD

Top 3 most demanded categories

🤝 Techniques:

pandas groupby, sum, merge

CSV export via to_csv()

✨ Improvements:

Use unit tests to validate metrics

Generate dashboards via Jupyter or Tableau

🧰 Challenge 3: PostgreSQL Loading + SQL Analysis

✅ Part A: Programmatic Ingestion

PostgreSQL used locally with SQLAlchemy

Data loaded from CSV into products and orders

Used FOREIGN KEY (product_id) REFERENCES products(product_id) to ensure referential integrity

✅ Part B: SQL KPIs

SQL file challenge_3_kpi_queries.sql includes:

Max order date

Most demanded product with ROUND() conversion fix

Top 3 categories

📈 Performance Optimizations:

Created indexes on created_date, product_id, category

Recommended materialized views for heavy aggregations

Used LIMIT to reduce scan overhead

Suggest table partitioning by date in large datasets

🌐 Governance Considerations:

Add metadata table for refresh timestamps

Enforce data typing with column constraints

Use schema versioning for evolutive changes

✨ Improvements:

Validate integrity with triggers

Schedule data refresh via Airflow or cron

🤖 Challenge 4: Strategic Proposal

Contained in challenge_4_proposal.md. Summary:

✨ Additional Business Insights:

Revenue per day (trend detection)

Average ticket per order

Product with highest day-to-day growth

⚖️ ELT Architecture:

Tool: Airbyte + dbt + BigQuery

Flow: Extract (Postgres) → Load (BigQuery) → Transform (dbt)

🧠 AI-Based Pipeline:

Model: Demand forecasting with regression (XGBoost or sklearn)

Input features: date, category, price, lag features

Output: Demand per product for X days

Deployment: Vertex AI Pipelines or SageMaker

🚀 Project Setup

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

📧 Author

Felipe OlivaresGitHub: @FelipeOlivaresM