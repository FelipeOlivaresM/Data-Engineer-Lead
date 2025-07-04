-- Challenge 3: SQL Queries for KPIs
-- Database: lead_data_test

-- 1. Date with most orders
SELECT created_date AS max_order_date, COUNT(*) AS order_count
FROM orders
GROUP BY created_date
ORDER BY order_count DESC
LIMIT 1;


-- 2. Most demanded product
SELECT 
    p.name AS most_demanded_product,
    SUM(o.quantity) AS total_quantity
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.name
ORDER BY total_quantity DESC
LIMIT 1;




-- 3. Top 3 most demanded categories
SELECT 
    p.category,
    SUM(o.quantity) AS total_quantity
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_quantity DESC
LIMIT 3;
