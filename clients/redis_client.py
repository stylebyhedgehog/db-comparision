# 1. Пользователи
# Ключи:
# user:{user_id}: Хранит информацию о пользователе в формате Hash.
# users: Множество (Set), содержащее все user_id для быстрого перечисления.
# Пример:
# user:1 -> { "name": "Alice", "email": "alice@example.com" }
# users -> {"1", "2", "3"}
#
# 2. Заказы
# Ключи:
# order:{order_id}: Хранит информацию о заказе в формате Hash. Поле items сериализуется в JSON для хранения состава заказа.
# user:{user_id}:orders: Множество (Set), содержащее все order_id пользователя.
# Пример:
# order:1 -> { "user_id": "1", "items": '[{"product_id": "1", "quantity": 1}]' }
# user:1:orders -> {"1"}
#
# 3. Продукты
# Ключи:
# product:{product_id}: Хранит информацию о продукте в формате Hash.
# category:{category_id}:products: Множество (Set), содержащее все product_id в указанной категории.
# Пример:
# product:1 -> { "name": "Laptop", "price": "1200.00", "category_id": "1" }
# category:1:products -> {"1"}
import logging
import os
import redis
import json

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

class RedisClient:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")  # значение по умолчанию
        redis_port = int(os.getenv("REDIS_PORT", 6379))  # значение по умолчанию
        redis_db = int(os.getenv("REDIS_DB", 0))  # значение по умолчанию

        self.client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        logger.info(f"Подключение к Redis установлено на {redis_host}:{redis_port}.")

    def create_user(self, user_id, name, email):
        user_key = f"user:{user_id}"
        self.client.hset(user_key, mapping={"name": name, "email": email})
        self.client.sadd("users", user_id)
        logger.info(f"Пользователь с ID {user_id} ({name}, {email}) успешно создан в Redis.")

    def get_user(self, user_id):
        user_key = f"user:{user_id}"
        user_data = self.client.hgetall(user_key)
        if user_data:
            logger.info(f"Пользователь с ID {user_id} найден в Redis: {user_data}")
        else:
            logger.info(f"Пользователь с ID {user_id} не найден в Redis.")
        return user_data

    def delete_user(self, user_id):
        user_key = f"user:{user_id}"
        self.client.delete(user_key)
        self.client.srem("users", user_id)
        logger.info(f"Пользователь с ID {user_id} удалён из Redis.")

    def create_order(self, order_id, user_id, items):
        order_key = f"order:{order_id}"
        self.client.hset(order_key, mapping={"user_id": user_id, "items": json.dumps(items)})
        self.client.sadd(f"user:{user_id}:orders", order_id)
        logger.info(f"Заказ с ID {order_id} для пользователя {user_id} добавлен в Redis.")

    def get_orders_by_user_id(self, user_id):
        order_ids = self.client.smembers(f"user:{user_id}:orders")
        orders = []
        for order_id in order_ids:
            order_key = f"order:{order_id}"
            order_data = self.client.hgetall(order_key)
            if order_data:
                order_data["items"] = json.loads(order_data["items"])
                orders.append(order_data)
        logger.info(f"Получены заказы для пользователя с ID {user_id} из Redis: {orders}")
        return orders

    def delete_order(self, order_id):
        order_key = f"order:{order_id}"
        order_data = self.client.hgetall(order_key)
        if order_data:
            user_id = order_data["user_id"]
            self.client.srem(f"user:{user_id}:orders", order_id)
        self.client.delete(order_key)
        logger.info(f"Заказ с ID {order_id} удалён из Redis.")

    def create_product(self, product_id, name, price, category_id):
        product_key = f"product:{product_id}"
        self.client.hset(product_key, mapping={"name": name, "price": price, "category_id": category_id})
        self.client.sadd(f"category:{category_id}:products", product_id)
        logger.info(f"Продукт с ID {product_id} ({name}, {price}) добавлен в Redis в категорию {category_id}.")

    def get_products_by_category_id(self, category_id):
        product_ids = self.client.smembers(f"category:{category_id}:products")
        products = []
        for product_id in product_ids:
            product_key = f"product:{product_id}"
            product_data = self.client.hgetall(product_key)
            if product_data:
                products.append(product_data)
        logger.info(f"Получены продукты из категории {category_id} в Redis: {products}")
        return products

    def delete_product(self, product_id):
        product_key = f"product:{product_id}"
        product_data = self.client.hgetall(product_key)
        if product_data:
            category_id = product_data["category_id"]
            self.client.srem(f"category:{category_id}:products", product_id)
        self.client.delete(product_key)
        logger.info(f"Продукт с ID {product_id} удалён из Redis.")

    def create_category(self, category_id, name):
        category_key = f"category:{category_id}"
        self.client.hset(category_key, mapping={"name": name})
        logger.info(f"Категория с ID {category_id} ({name}) добавлена в Redis.")

    def get_category(self, category_id):
        category_key = f"category:{category_id}"
        category_data = self.client.hgetall(category_key)
        if category_data:
            logger.info(f"Категория с ID {category_id} найдена в Redis: {category_data}")
        else:
            logger.info(f"Категория с ID {category_id} не найдена в Redis.")
        return category_data

    def delete_category(self, category_id):
        category_key = f"category:{category_id}"
        self.client.delete(category_key)
        logger.info(f"Категория с ID {category_id} удалена из Redis.")

    def get_purchased_products_by_user_id(self, user_id):
        orders = self.get_orders_by_user_id(user_id)
        product_ids = set()
        for order in orders:
            for item in order["items"]:
                product_ids.add(item["product_id"])
        products = []
        for product_id in product_ids:
            product_key = f"product:{product_id}"
            product_data = self.client.hgetall(product_key)
            if product_data:
                product_data["product_id"] = product_id  # Добавляем product_id в данные
                products.append(product_data)
        logger.info(f"Получены продукты, купленные пользователем с ID {user_id}: {products}")
        return products

    def get_users_with_similar_purchases(self, user_id):
        user_products = {item["product_id"] for item in self.get_purchased_products_by_user_id(user_id)}
        all_users = self.client.smembers("users")
        similar_users = []
        for other_user_id in all_users:
            if other_user_id == user_id:
                continue

            other_user_products = {item["product_id"] for item in self.get_purchased_products_by_user_id(other_user_id)}
            if user_products & other_user_products:
                similar_users.append(self.get_user(other_user_id))

        logger.info(f"Найдено пользователей с похожими покупками для пользователя с ID {user_id}: {similar_users}")
        return similar_users
