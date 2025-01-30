CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    data JSONB NOT NULL DEFAULT '{}' -- Пример: { "name": "John Doe", "email": "john.doe@example.com", "registration_date": "2025-01-01" }
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    items JSONB NOT NULL DEFAULT '[]', -- Пример: [ { "product_id": 1, "quantity": 2 }, { "product_id": 3, "quantity": 1 } ]
    data JSONB NOT NULL DEFAULT '{}' -- Пример: { "order_date": "2025-01-15", "total": 150.00 }
);

CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    data JSONB NOT NULL DEFAULT '{}' -- Пример: { "name": "Smartphone", "price": 599.99, "category_name": "Electronics" }
);
