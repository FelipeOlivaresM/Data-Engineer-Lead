
SELECT 
    ROUND(SUM(p.price * o.quantity)::numeric, 2) / COUNT(DISTINCT o.order_id) AS avg_ticket_per_order
FROM orders o
JOIN products p ON o.product_id = p.product_id;