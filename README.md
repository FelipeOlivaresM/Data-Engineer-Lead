# 🧠 Lead Data Engineer Technical Assessment 

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
│   ├── Challenge_1.py  
│   ├── Challenge_2.py  
│   ├── Challenge_2_2.py  
│   ├── Challenge_3.py    
│   ├── challenge_3_create_indexes.sql  
│   ├── Challenge_3_KPIs_queries.sql  
│   └── Test DF scripts.ipynb #Jupiter notebook for testing  
│   └── Challenge_4_proposal.md

│  
├── .env                    # Environment variables (excluded from Git)  
├── .gitignore  
├── requirements.txt  
└── README.md               # This file  


-----------------------------------------------------------------------------------------------------------------------------------

🌟 Challenge 1: Merging Orders and Products Data

✅ Goal:

Merge orders.csv and products.csv to generate order_full_information.csv with:

  * order_created_date
  * order_id
  * product_name
  * quantity
  * total_price (calculated as price * quantity)

🛠️ Tools:

  * Python
  * pandas

📃 Implementation:

  * Load both CSVs
  * Merge on product_id
  * Calculate total price

    
Note: It is important to mention that the date field is formatted, since the date format has quotes in the initial files.

Format columns and export CSV ~> outputs/order_full_information.csv

-----------------------------------------------------------------------------------------------------------------------------------

🌟 Challenge 2: Currency Conversion and KPIs

✅ Part A: BRL to USD Currency Conversion 

 * API: freecurrencyapi.com
 * API key loaded via .env
 
 Generated fixed_order_full_information.csv with:
  * total_price_br
  * total_price_us (using real-time rate)


📃 Implementation:

  * Load the base file ~> outputs/order_full_information.csv
  * Load the API key securely
  * Fetch exchange rate from API (Includes error handling in production.)
  * Convert total_price to USD (Simple column-wise multiplication)
  * Export updated dataset (This file is now the input for KPI generation ~> outputs/fixed_order_full_information.csv)

    
✅ Part B: KPIs Generation

 Produced kpi_product_orders.csv with:
  * Date with the highest number of orders
  * Most demanded product + total sales in USD
  * Top 3 most demanded categories

🛠️ Tools & Techniques:

 * pandas
 * groupby, sum, merge
 * CSV export via to_csv()

📃 Implementation:

  * Load the enriched dataset (outputs/fixed_order_full_information.csv) 
  * KPI 1 – Date with highest order volume (Groups by date and counts order IDs, idxmax() returns the date with the most orders)
  * KPI 2 – Most demanded product and its sales (Extracts the product with the highest demand and total USD sales)
  * KPI 3 – Top 3 categories by quantity (Groups by category, sums the quantity, selects top 3 - Joins them into a single string for reporting.)
  * Export KPIs (CSV - Clean and clear KPI structure) 

-----------------------------------------------------------------------------------------------------------------------------------
    
🌟 Challenge 3: PostgreSQL Loading + SQL Analysis

✅ Part A: Programmatic Ingestion

PostgreSQL used locally with SQLAlchemy

* Secure environment configuration
* Data loaded from CSV into products and orders
* Schema creation (CHECK constraints enforce data integrity at DB level - fOREIGN KEY enforces referential consistency - Tables are only created if they don’t exist—safe for re-execution.)
* Used FOREIGN KEY (product_id) REFERENCES products(product_id) to ensure referential integrity
* Validation before insertion (Keeps a traceable copy in outputs/invalid_*.csv)
* Insert data into PostgreSQL (if_exists="append" ensures table is reused without dropping it.)
 

✅ Part B: SQL KPIs

SQL file challenge_3_kpi_queries.sql includes:

Max order date
Most demanded product with ROUND() conversion fix
Top 3 categories


📈 Performance Optimizations:

 * Created indexes on created_date, product_id, category (Index Suggestions (included in SQL script)
 * Recommended materialized views for heavy aggregations (Especially important on large datasets millions of rows)
 * Used LIMIT to reduce scan overhead
 * Table partitioning by date in large datasets

🌐 Governance Considerations:

 * Add metadata table for refresh timestamps
 * Enforce data typing with column constraints
 * All invalid data is logged and exported before loading.
 * Use schema versioning for evolutive changes

✨ Improvements:

 * Validate integrity with triggers
 * Schedule data refresh via Airflow or cron or windows task

-----------------------------------------------------------------------------------------------------------------------------------

🤖 Challenge 4: Strategic Proposal

Summary:

✨ Additional Business Insights:

Revenue per day (trend detection):
   * Total daily revenue aggregated by order_created_date. This allows us to see how sales evolve over time
 Why is it useful?
   * Detects growth or decline trends in revenue.
   * Helps measure the impact of campaigns, seasonality, or outages.
   * Supports forecasting models and capacity planning.
   * Useful for reporting KPIs like daily performance or pipeline alerts.
How to get it
   * scripts/Challenge_4_1insights.sql

Average ticket per order
   * The average revenue per order, that is, the total revenue divided by the total number of orders.
Why is it useful?   
   * Indicates customer spending behavior.
   * Helps track basket size and efficiency of sales.
   * Used to measure upselling effectiveness.
   * Can inform pricing strategy or discount decisions.
How to get it
   * scripts/Challenge_4_2insights.sql

Note: It's important consider creating a derived table order_summary if it plan to use this metric frequently

Product with highest day-to-day growth
   * The product whose quantity sold increased the most from one day to the next.
Why is it useful?   
   * Detects emerging bestsellers or virality.
   * Great for inventory alerting, trend tracking, and campaign optimization.
   * Helps identify seasonal winners or the result of recent promotions.
How to get it
   * scripts/Challenge_4_3insights.sql

Note: This insight could be enhanced with a windowed moving average or used to power an AI model for demand prediction.

-----------------------------------------------------------------------------------------------------------------------------------

✨ ELT Architecture:
 
 I recommend using an ELT because it leverages BigQuery's compute engine and decouples extraction and transformation, which is ideal for flexibility, governance, and scale.
 
 Tool: Airbyte + dbt + BigQuery
  
  * Extraction & Loading: Airbyte:
     *  Open-source, easy to deploy
     *  Native connectors for PostgreSQL → BigQuery
  * Transformation: dbt (Data Build Tool)
     *  Facilitates CI/CD pipelines and documentation
     *  Enables testing, validation and column typing
   
  * Flow Diagram
     *  PostgreSQL → (Extract & Load via Airbyte) → BigQuery (raw tables)
     *  BigQuery (raw) → (Transform via dbt) → BigQuery (modeled tables/views)


Steps to create the pipeline proposed

Step 1: 
 * Prepare the Source Data
 * Ensure PostgreSQL is running and accessible.
 * Normalize and clean tables like orders and products.
 * Apply constraints (e.g., CHECK, FOREIGN KEY) for integrity.
 * Optionally, create views or summary tables to optimize extraction.

Step 2: 
 * Set Up the Extraction Tool (Airbyte)
 * Deploy Airbyte (Docker or Cloud).
 * Configure a PostgreSQL Source Connector: Set credentials, database name, tables to extract.
 * Configure a BigQuery Destination Connector: (Provide service account JSON - Choose destination dataset)
 * Define sync schedule (e.g., every hour, daily).
 * Run an initial sync and validate sample rows.

Step 3: 
 * Load into BigQuery (Raw Tables)
 * Airbyte will load raw tables into bigquery.dataset._airbyte_raw_*.
 * Inspect the structure in BigQuery UI.
 * Enable partitioning by created_date if the table supports it.

Step 4:
 * Transform Data Using dbt
 * Initialize a dbt project (dbt init).
 * Configure BigQuery profile using service account credentials.
 * Add dbt tests: unique, not null, and relationships.

Step 5: 
 * Orchestrate the Pipeline
 * Option 1: Use Airbyte Scheduler and dbt Cloud jobs.
 * Option 2: Use Apache Airflow or Prefect to control: Airbyte sync jobs - dbt transformations - Slack/Email alerts

Step 6: 
 * Validate, Monitor and Automate
 * Enable dbt documentation (dbt docs generate)
 * Use Airbyte sync history + alerts
 * Set up CI/CD to auto-deploy dbt models on Git push
 * Audit table refresh timestamps for SLA control

-----------------------------------------------------------------------------------------------------------------------------------

🧠 AI-Based Pipeline:

Model: Product Demand Forecasting

Objetive: Forecast daily demand per product to optimize stock, pricing, and production planning

From BigQuery (dbt models):
 * product_id
 * created_date
 * quantity
 * price
 * category

Enriched with:

 * Calendar features (weekend, holiday, day-of-week)
 * Lag features (previous demand)

Model Type:
 * Regression model (e.g., XGBoost, RandomForest, or LSTM for time-series)
 * Target variable: quantity (next-day or 7-day rolling forecast)

-----------------------------------------------------------------------------------------------------------------------------------

Integration Steps:
Data prep with dbt:
 * Create a model: product_demand_features.sql
 * Include historical aggregations (moving averages, lag features)
   
Export to Vertex AI or SageMaker:
 * Use scheduled BigQuery export to GCS
 * Load into AI platform for training

Train the model:
 * Use scikit-learn or xgboost
 * Evaluate with RMSE, MAE

Serve predictions:
 * Store output table: predicted_product_demand
 * Join back with dashboards or alerts

Automate pipeline:
 * Use Airflow or Prefect to trigger: Data refresh → Model train → Prediction insert

Value to Bussiness:
 * Reduces overstock or understock risk
 * Supports just-in-time supply chain decisions
 * Enables proactive marketing and pricing strategies
 * Can be scaled to per-region, per-category forecasts

-----------------------------------------------------------------------------------------------------------------------------------

🚀 Project Setup

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

📧 Author

Felipe OlivaresGitHub: @FelipeOlivaresM
