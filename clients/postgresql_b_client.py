import os
import psycopg2
from psycopg2.extras import Json
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

class PostgreSQLBClient:
    def __init__(self):
        database_url = os.getenv('DATABASE_JSONB_URL')
        if not database_url:
            raise ValueError("DATABASE_URL is not set in the environment")
        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()
        logging.info("Подключение к базе данных PostgreSQL установлено")

    def create_user(self, name, email, registration_date):
        data = {"name": name, "email": email, "registration_date": registration_date}
        query = """INSERT INTO Users (data) VALUES (%s) RETURNING user_id"""
        self.cursor.execute(query, (Json(data),))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Пользователь {name} с email {email} успешно создан с ID: {user_id}")
        return user_id

    def get_user(self, user_id):
        query = """SELECT data FROM Users WHERE user_id = %s"""
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        logging.info(f"Пользователь с ID {user_id} найден: {result}")
        return result[0] if result else None

    def create_product(self, name, price, category_name):
        data = {"name": name, "price": price, "category_name": category_name}
        query = """INSERT INTO Products (data) VALUES (%s) RETURNING product_id"""
        self.cursor.execute(query, (Json(data),))
        product_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Продукт {name} с ценой {price} успешно создан с ID: {product_id}")
        return product_id

    def get_product(self, product_id):
        query = """SELECT data FROM Products WHERE product_id = %s"""
        self.cursor.execute(query, (product_id,))
        result = self.cursor.fetchone()
        logging.info(f"Продукт с ID {product_id} найден: {result}")
        return result[0] if result else None

    def create_order(self, user_id, items, order_date, total):
        items_data = [{"product_id": item["product_id"], "quantity": item["quantity"]} for item in items]
        data = {"order_date": order_date, "total": total}
        query = """INSERT INTO Orders (user_id, items, data) VALUES (%s, %s, %s) RETURNING order_id"""
        self.cursor.execute(query, (user_id, Json(items_data), Json(data)))
        order_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Заказ с ID {order_id} для пользователя с ID {user_id} создан")
        return order_id

    def get_order(self, order_id):
        query = """SELECT user_id, items, data FROM Orders WHERE order_id = %s"""
        self.cursor.execute(query, (order_id,))
        result = self.cursor.fetchone()
        logging.info(f"Заказ с ID {order_id} найден: {result}")
        return result if result else None

    def get_orders_by_user_id(self, user_id):
        query = """SELECT order_id, data FROM Orders WHERE user_id = %s"""
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        logging.info(f"Заказы пользователя с ID {user_id}: {result}")
        return result

    def get_products_by_user_id(self, user_id):
        query = """
        SELECT DISTINCT p.product_id, p.data
        FROM Products p
        JOIN Orders o ON o.user_id = %s
        JOIN jsonb_array_elements(o.items) as item
            ON (item->>'product_id')::INT = p.product_id
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        logging.info(f"Продукты, купленные пользователем с ID {user_id}: {result}")
        return result

    def get_users_with_similar_purchases(self, user_id):
        query = """
        SELECT DISTINCT (item->>'product_id')::INT as product_id
        FROM Orders
        JOIN jsonb_array_elements(items) as item ON true
        WHERE user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        purchased_products = [row[0] for row in self.cursor.fetchall()]

        if not purchased_products:
            logging.info("Пользователь не сделал покупок")
            return []

        query = """
        SELECT DISTINCT u.user_id, u.data->>'name'
        FROM Users u
        JOIN Orders o ON u.user_id = o.user_id
        JOIN jsonb_array_elements(o.items) as item
            ON (item->>'product_id')::INT = ANY(%s)
        WHERE u.user_id != %s
        """
        self.cursor.execute(query, (purchased_products, user_id))
        result = self.cursor.fetchall()
        logging.info(f"Пользователи с похожими покупками: {result}")
        return result

    def get_products_by_category_id(self, category_name):
        query = """SELECT product_id, data FROM Products WHERE data->>'category_name' = %s"""
        self.cursor.execute(query, (category_name,))
        result = self.cursor.fetchall()
        logging.info(f"Продукты в категории {category_name}: {result}")
        return result