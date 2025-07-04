-- Index to improve performance

-- Index for faster queries on created_date
CREATE INDEX IF NOT EXISTS idx_orders_created_date
ON orders (created_date);

-- Index for better joins between orders and products
CREATE INDEX IF NOT EXISTS idx_orders_product_id
ON orders (product_id);

-- Index for faster queries on product category
CREATE INDEX IF NOT EXISTS idx_products_category
ON products (category);
