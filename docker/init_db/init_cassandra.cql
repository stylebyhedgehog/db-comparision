CREATE KEYSPACE IF NOT EXISTS test_keyspace
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};


CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    registration_date DATE
);

CREATE TABLE IF NOT EXISTS orders_by_user (
    user_id UUID,
    order_id UUID,
    order_date DATE,
    total DECIMAL,
    PRIMARY KEY (user_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC);

CREATE TABLE IF NOT EXISTS order_items_by_order (
    order_id UUID,
    product_id UUID,
    product_name TEXT,
    price DECIMAL,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS products_by_category (
    category_id UUID,
    product_id UUID,
    product_name TEXT,
    price DECIMAL,
    PRIMARY KEY (category_id, product_id)
);

CREATE TABLE IF NOT EXISTS products_by_user (
    user_id UUID,
    product_id UUID,
    product_name TEXT,
    price DECIMAL,
    PRIMARY KEY ((product_id), user_id)
);
