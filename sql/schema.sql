DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    amount FLOAT,
    order_date DATE
);

INSERT INTO orders (customer_name, product_id, product_name, amount, order_date) VALUES ("Atmiya Patel", 1234, "MacBook", 2000.99, "2025-07-30");
