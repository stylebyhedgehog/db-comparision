# Коллекция users:
# {
#   "_id": ObjectId("..."),
#   "name": "John",
#   "email": "john@example.com",
#   "registration_date": "2024-12-20"
# }
# Коллекция orders:
# {
#   "_id": ObjectId("..."),
#   "user_id": ObjectId("..."),
#   "order_date": "2024-12-20",
#   "total": 150.00,
#   "items": [
#     { "product_id": ObjectId("..."), "quantity": 2 }
#   ]
# }
# Коллекция products:
# {
#   "_id": ObjectId("..."),
#   "name": "Product A",
#   "price": 50.00,
#   "category_id": ObjectId("...")
# }
# Коллекция categories:
# {
#   "_id": ObjectId("..."),
#   "category_name": "Electronics"
# }


import os
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

class MongoDBClient:
    def __init__(self):
        mongo_url = os.getenv('MONGO_URL')
        if not mongo_url:
            raise ValueError("MONGO_URL is not set in the environment")

        self.client = MongoClient(mongo_url)
        self.db = self.client.get_database("ecommerce")
        logging.info("Подключение к MongoDB установлено")

    def create_user(self, name, email, registration_date):
        result = self.db.users.insert_one({"name": name, "email": email, "registration_date": registration_date})
        user_id = result.inserted_id
        logging.info(f"Пользователь {name} с email {email} успешно создан с ID: {user_id}")
        return user_id

    def get_user(self, user_id):
        user = self.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            logging.info(f"Пользователь с ID {user_id} найден: {user}")
        else:
            logging.info(f"Пользователь с ID {user_id} не найден")
        return user

    def update_user(self, user_id, name=None, email=None, registration_date=None):
        update_fields = {key: value for key, value in {"name": name, "email": email, "registration_date": registration_date}.items() if value is not None}
        result = self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
        logging.info(f"Данные пользователя с ID {user_id} обновлены, изменено записей: {result.modified_count}")

    def delete_user(self, user_id):
        result = self.db.users.delete_one({"_id": ObjectId(user_id)})
        logging.info(f"Пользователь с ID {user_id} удалён, удалено записей: {result.deleted_count}")

    def create_order(self, user_id, order_date, total, items):
        result = self.db.orders.insert_one({"user_id": ObjectId(user_id), "order_date": order_date, "total": total, "items": items})
        order_id = result.inserted_id
        logging.info(f"Заказ для пользователя с ID {user_id} на сумму {total} успешно создан с ID: {order_id}")
        return order_id

    def get_order(self, order_id):
        order = self.db.orders.find_one({"_id": ObjectId(order_id)})
        if order:
            logging.info(f"Заказ с ID {order_id} найден: {order}")
        else:
            logging.info(f"Заказ с ID {order_id} не найден")
        return order

    def update_order(self, order_id, user_id=None, order_date=None, total=None, items=None):
        update_fields = {key: value for key, value in {"user_id": ObjectId(user_id) if user_id else None, "order_date": order_date, "total": total, "items": items}.items() if value is not None}
        result = self.db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": update_fields})
        logging.info(f"Данные заказа с ID {order_id} обновлены, изменено записей: {result.modified_count}")

    def delete_order(self, order_id):
        result = self.db.orders.delete_one({"_id": ObjectId(order_id)})
        logging.info(f"Заказ с ID {order_id} удалён, удалено записей: {result.deleted_count}")

    def create_product(self, name, price, category_id):
        result = self.db.products.insert_one({"name": name, "price": price, "category_id": ObjectId(category_id)})
        product_id = result.inserted_id
        logging.info(f"Продукт {name} с ценой {price} успешно создан с ID: {product_id}")
        return product_id

    def get_product(self, product_id):
        product = self.db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            logging.info(f"Продукт с ID {product_id} найден: {product}")
        else:
            logging.info(f"Продукт с ID {product_id} не найден")
        return product

    def update_product(self, product_id, name=None, price=None, category_id=None):
        update_fields = {key: value for key, value in {"name": name, "price": price, "category_id": ObjectId(category_id) if category_id else None}.items() if value is not None}
        result = self.db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_fields})
        logging.info(f"Данные продукта с ID {product_id} обновлены, изменено записей: {result.modified_count}")

    def delete_product(self, product_id):
        result = self.db.products.delete_one({"_id": ObjectId(product_id)})
        logging.info(f"Продукт с ID {product_id} удалён, удалено записей: {result.deleted_count}")

    def create_category(self, category_name):
        result = self.db.categories.insert_one({"category_name": category_name})
        category_id = result.inserted_id
        logging.info(f"Категория {category_name} успешно создана с ID: {category_id}")
        return category_id

    def get_category(self, category_id):
        category = self.db.categories.find_one({"_id": ObjectId(category_id)})
        if category:
            logging.info(f"Категория с ID {category_id} найдена: {category}")
        else:
            logging.info(f"Категория с ID {category_id} не найдена")
        return category

    def update_category(self, category_id, category_name):
        result = self.db.categories.update_one({"_id": ObjectId(category_id)}, {"$set": {"category_name": category_name}})
        logging.info(f"Категория с ID {category_id} обновлена, изменено записей: {result.modified_count}")

    def delete_category(self, category_id):
        result = self.db.categories.delete_one({"_id": ObjectId(category_id)})
        logging.info(f"Категория с ID {category_id} удалена, удалено записей: {result.deleted_count}")

    def get_orders_by_user_id(self, user_id):
        orders = list(self.db.orders.find({"user_id": ObjectId(user_id)}))
        logging.info(f"Заказы пользователя с ID {user_id}: {orders}")
        return orders

    def get_purchased_products_by_user_id(self, user_id):
        orders = self.get_orders_by_user_id(user_id)
        product_ids = [item["product_id"] for order in orders for item in order["items"]]
        products = list(self.db.products.find({"_id": {"$in": product_ids}}))
        logging.info(f"Продукты, купленные пользователем с ID {user_id}: {products}")
        return products

    def get_users_with_similar_purchases(self, user_id):
        user_products = self.get_purchased_products_by_user_id(user_id)
        user_product_ids = {product["_id"] for product in user_products}

        orders = list(self.db.orders.find())
        similar_user_ids = set()

        for order in orders:
            order_product_ids = {item["product_id"] for item in order["items"]}
            if user_product_ids & order_product_ids:
                similar_user_ids.add(order["user_id"])

        similar_users = list(self.db.users.find({"_id": {"$in": list(similar_user_ids)}}))
        logging.info(f"Пользователи с похожими покупками: {similar_users}")
        return similar_users

    def get_products_by_category_id(self, category_id):
        products = list(self.db.products.find({"category_id": ObjectId(category_id)}))
        logging.info(f"Продукты в категории с ID {category_id}: {products}")
        return products


