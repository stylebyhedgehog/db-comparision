import os
import psycopg2
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class PostgreSQLClient:
    def __init__(self):
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL is not set in the environment")

        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()
        logging.info("Подключение к базе данных PostgreSQL установлено")

    def create_user(self, name, email, registration_date):
        query = """INSERT INTO Users (name, email, registration_date) VALUES (%s, %s, %s) RETURNING user_id"""
        self.cursor.execute(query, (name, email, registration_date))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Пользователь {name} с email {email} успешно создан с ID: {user_id}")
        return user_id

    def get_user(self, user_id):
        query = """SELECT * FROM Users WHERE user_id = %s"""
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if result:
            logging.info(f"Пользователь с ID {user_id} найден: {result}")
        else:
            logging.info(f"Пользователь с ID {user_id} не найден")
        return result

    def update_user(self, user_id, name=None, email=None, registration_date=None):
        query = """UPDATE Users SET name = COALESCE(%s, name), email = COALESCE(%s, email), registration_date = COALESCE(%s, registration_date) WHERE user_id = %s"""
        self.cursor.execute(query, (name, email, registration_date, user_id))
        self.connection.commit()
        logging.info(f"Данные пользователя с ID {user_id} обновлены")

    def delete_user(self, user_id):
        query = """DELETE FROM Users WHERE user_id = %s"""
        self.cursor.execute(query, (user_id,))
        self.connection.commit()
        logging.info(f"Пользователь с ID {user_id} удалён")

    def create_order(self, user_id, order_date, total):
        query = """INSERT INTO Orders (user_id, order_date, total) VALUES (%s, %s, %s) RETURNING order_id"""
        self.cursor.execute(query, (user_id, order_date, total))
        order_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Заказ для пользователя с ID {user_id} на сумму {total} успешно создан с ID: {order_id}")
        return order_id

    def get_order(self, order_id):
        query = """SELECT * FROM Orders WHERE order_id = %s"""
        self.cursor.execute(query, (order_id,))
        result = self.cursor.fetchone()
        if result:
            logging.info(f"Заказ с ID {order_id} найден: {result}")
        else:
            logging.info(f"Заказ с ID {order_id} не найден")
        return result

    def update_order(self, order_id, user_id=None, order_date=None, total=None):
        query = """UPDATE Orders SET user_id = COALESCE(%s, user_id), order_date = COALESCE(%s, order_date), total = COALESCE(%s, total) WHERE order_id = %s"""
        self.cursor.execute(query, (user_id, order_date, total, order_id))
        self.connection.commit()
        logging.info(f"Данные заказа с ID {order_id} обновлены")

    def delete_order(self, order_id):
        query = """DELETE FROM Orders WHERE order_id = %s"""
        self.cursor.execute(query, (order_id,))
        self.connection.commit()
        logging.info(f"Заказ с ID {order_id} удалён")

    def create_product(self, name, price, category_id):
        query = """INSERT INTO Products (name, price, category_id) VALUES (%s, %s, %s) RETURNING product_id"""
        self.cursor.execute(query, (name, price, category_id))
        product_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Продукт {name} с ценой {price} успешно создан с ID: {product_id}")
        return product_id

    def get_product(self, product_id):
        query = """SELECT * FROM Products WHERE product_id = %s"""
        self.cursor.execute(query, (product_id,))
        result = self.cursor.fetchone()
        if result:
            logging.info(f"Продукт с ID {product_id} найден: {result}")
        else:
            logging.info(f"Продукт с ID {product_id} не найден")
        return result

    def update_product(self, product_id, name=None, price=None, category_id=None):
        query = """UPDATE Products SET name = COALESCE(%s, name), price = COALESCE(%s, price), category_id = COALESCE(%s, category_id) WHERE product_id = %s"""
        self.cursor.execute(query, (name, price, category_id, product_id))
        self.connection.commit()
        logging.info(f"Данные продукта с ID {product_id} обновлены")

    def delete_product(self, product_id):
        query = """DELETE FROM Products WHERE product_id = %s"""
        self.cursor.execute(query, (product_id,))
        self.connection.commit()
        logging.info(f"Продукт с ID {product_id} удалён")

    def create_category(self, category_name):
        query = """INSERT INTO Categories (category_name) VALUES (%s) RETURNING category_id"""
        self.cursor.execute(query, (category_name,))
        category_id = self.cursor.fetchone()[0]
        self.connection.commit()
        logging.info(f"Категория {category_name} успешно создана с ID: {category_id}")
        return category_id

    def get_category(self, category_id):
        query = """SELECT * FROM Categories WHERE category_id = %s"""
        self.cursor.execute(query, (category_id,))
        result = self.cursor.fetchone()
        if result:
            logging.info(f"Категория с ID {category_id} найдена: {result}")
        else:
            logging.info(f"Категория с ID {category_id} не найдена")
        return result

    def update_category(self, category_id, category_name):
        query = """UPDATE Categories SET category_name = %s WHERE category_id = %s"""
        self.cursor.execute(query, (category_name, category_id))
        self.connection.commit()
        logging.info(f"Категория с ID {category_id} обновлена")

    def delete_category(self, category_id):
        query = """DELETE FROM Categories WHERE category_id = %s"""
        self.cursor.execute(query, (category_id,))
        self.connection.commit()
        logging.info(f"Категория с ID {category_id} удалена")

    def create_order_item(self, order_id, product_id, quantity):
        query = """INSERT INTO Order_Items (order_id, product_id, quantity) VALUES (%s, %s, %s)"""
        self.cursor.execute(query, (order_id, product_id, quantity))
        self.connection.commit()
        logging.info(f"Товар с ID {product_id} добавлен в заказ с ID {order_id} в количестве {quantity}")

    def get_order_items(self, order_id):
        query = """SELECT * FROM Order_Items WHERE order_id = %s"""
        self.cursor.execute(query, (order_id,))
        result = self.cursor.fetchall()
        logging.info(f"Товары для заказа с ID {order_id}: {result}")
        return result

    def delete_order_item(self, order_id, product_id):
        query = """DELETE FROM Order_Items WHERE order_id = %s AND product_id = %s"""
        self.cursor.execute(query, (order_id, product_id))
        self.connection.commit()
        logging.info(f"Товар с ID {product_id} удалён из заказа с ID {order_id}")

    def get_orders_by_user_id(self, user_id):
        query = """SELECT * FROM Orders WHERE user_id = %s"""
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        logging.info(f"Заказы пользователя с ID {user_id}: {result}")
        return result

    def get_products_by_user_id(self, user_id):
        query = """
        SELECT DISTINCT p.product_id, p.name, p.price
        FROM Products p
        JOIN Order_Items oi ON p.product_id = oi.product_id
        JOIN Orders o ON oi.order_id = o.order_id
        WHERE o.user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        logging.info(f"Продукты, купленные пользователем с ID {user_id}: {result}")
        return result

    def get_users_with_similar_purchases(self, user_id):
        query = """
        SELECT DISTINCT p.product_id
        FROM Products p
        JOIN Order_Items oi ON p.product_id = oi.product_id
        JOIN Orders o ON oi.order_id = o.order_id
        WHERE o.user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        purchased_products = [row[0] for row in self.cursor.fetchall()]

        if not purchased_products:
            logging.info("Пользователь не сделал покупок")
            return []

        query = """
        SELECT DISTINCT u.user_id, u.name
        FROM Users u
        JOIN Orders o ON u.user_id = o.user_id
        JOIN Order_Items oi ON o.order_id = oi.order_id
        WHERE oi.product_id IN %s AND u.user_id != %s
        """
        self.cursor.execute(query, (tuple(purchased_products), user_id))
        result = self.cursor.fetchall()
        logging.info(f"Пользователи с похожими покупками: {result}")
        return result

    def get_products_by_category_id(self, category_id):
        query = """SELECT * FROM Products WHERE category_id = %s"""
        self.cursor.execute(query, (category_id,))
        result = self.cursor.fetchall()
        logging.info(f"Продукты в категории с ID {category_id}: {result}")
        return result
