WITH product_daily AS (
    SELECT 
        o.product_id,
        p.name,
        o.created_date,
        SUM(o.quantity) AS daily_quantity
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY o.product_id, p.name, o.created_date
),
growth_calc AS (
    SELECT 
        product_id,
        name,
        created_date,
        daily_quantity,
        LAG(daily_quantity) OVER (PARTITION BY product_id ORDER BY created_date) AS prev_day_quantity,
        (daily_quantity - LAG(daily_quantity) OVER (PARTITION BY product_id ORDER BY created_date)) AS growth
    FROM product_daily
)
SELECT 
    name,
    created_date,
    growth
FROM growth_calc
WHERE growth IS NOT NULL
ORDER BY growth DESC
LIMIT 1;