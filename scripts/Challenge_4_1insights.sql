SELECT 
    created_date, 
    ROUND(SUM(p.price * o.quantity)::numeric, 2) AS daily_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY created_date
ORDER BY created_date;
