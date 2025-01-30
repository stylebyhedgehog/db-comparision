# CREATE (u:User {user_id: "1", name: "John Doe", email: "john.doe@example.com", registration_date: "2023-01-01"});
# CREATE (o:Order {order_id: "1", order_date: "2023-01-10", total: 100.00});
# CREATE (p:Product {product_id: "101", name: "Product A", price: 50.00});
# CREATE (c:Category {category_id: "10", category_name: "Electronics"});
#
# CREATE (u)-[:PLACED]->(o);
# CREATE (o)-[:CONTAINS]->(p);
# CREATE (p)-[:BELONGS_TO]->(c);


import os
import logging
from neo4j import GraphDatabase

# Настройка логирования
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)  # Настройка базового уровня логирования

class Neo4jClient:
    def __init__(self):
        NEO4J_URI = os.getenv("NEO4J_URI")
        NEO4J_USER = os.getenv("NEO4J_USER")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

        if not NEO4J_URI or not NEO4J_USER or not NEO4J_PASSWORD:
            raise ValueError("NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set in the environment")

        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        logging.info("Подключение к базе данных Neo4j установлено")

    def close(self):
        self.driver.close()
        logging.info("Подключение к базе данных Neo4j закрыто")

    def create_user(self, user_id, name, email, registration_date):
        query = """
        CREATE (u:User {user_id: $user_id, name: $name, email: $email, registration_date: $registration_date})
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, name=name, email=email, registration_date=registration_date)
            logging.info(f"Создан пользователь с ID {user_id}, имя: {name}, email: {email}")
            return result.single()["u"]

    def get_user(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            user = result.single()
            if user:
                logging.info(f"Найден пользователь с ID {user_id}")
            else:
                logging.warning(f"Пользователь с ID {user_id} не найден")
            return user["u"] if user else None

    def update_user(self, user_id, name=None, email=None, registration_date=None):
        query = """
        MATCH (u:User {user_id: $user_id})
        SET u += $updates
        RETURN u
        """
        updates = {k: v for k, v in {"name": name, "email": email, "registration_date": registration_date}.items() if v is not None}
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id, updates=updates)
            logging.info(f"Обновлены данные пользователя с ID {user_id}: {updates}")
            return result.single()["u"]

    def delete_user(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})
        DETACH DELETE u
        """
        with self.driver.session() as session:
            session.run(query, user_id=user_id)
            logging.info(f"Удалён пользователь с ID {user_id}")

    def create_order(self, order_id, order_date, total, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})
        CREATE (o:Order {order_id: $order_id, order_date: $order_date, total: $total})
        CREATE (u)-[:PLACED]->(o)
        RETURN o
        """
        with self.driver.session() as session:
            result = session.run(query, order_id=order_id, order_date=order_date, total=total, user_id=user_id)
            logging.info(f"Создан заказ с ID {order_id} на сумму {total} для пользователя с ID {user_id}")
            return result.single()["o"]

    def get_order(self, order_id):
        query = """
        MATCH (o:Order {order_id: $order_id})
        RETURN o
        """
        with self.driver.session() as session:
            result = session.run(query, order_id=order_id)
            order = result.single()
            if order:
                logging.info(f"Найден заказ с ID {order_id}")
            else:
                logging.warning(f"Заказ с ID {order_id} не найден")
            return order["o"] if order else None

    def update_order(self, order_id, order_date=None, total=None):
        query = """
        MATCH (o:Order {order_id: $order_id})
        SET o += $updates
        RETURN o
        """
        updates = {k: v for k, v in {"order_date": order_date, "total": total}.items() if v is not None}
        with self.driver.session() as session:
            result = session.run(query, order_id=order_id, updates=updates)
            logging.info(f"Обновлены данные заказа с ID {order_id}: {updates}")
            return result.single()["o"]

    def delete_order(self, order_id):
        query = """
        MATCH (o:Order {order_id: $order_id})
        DETACH DELETE o
        """
        with self.driver.session() as session:
            session.run(query, order_id=order_id)
            logging.info(f"Удалён заказ с ID {order_id}")

    def create_product(self, product_id, name, price, category_id):
        query = """
        MATCH (c:Category {category_id: $category_id})
        CREATE (p:Product {product_id: $product_id, name: $name, price: $price})
        CREATE (p)-[:BELONGS_TO]->(c)
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, product_id=product_id, name=name, price=price, category_id=category_id)
            logging.info(f"Создан продукт с ID {product_id}, имя: {name}, цена: {price}, категория ID {category_id}")
            return result.single()["p"]

    def get_product(self, product_id):
        query = """
        MATCH (p:Product {product_id: $product_id})
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, product_id=product_id)
            product = result.single()
            if product:
                logging.info(f"Найден продукт с ID {product_id}")
            else:
                logging.warning(f"Продукт с ID {product_id} не найден")
            return product["p"] if product else None

    def update_product(self, product_id, name=None, price=None):
        query = """
        MATCH (p:Product {product_id: $product_id})
        SET p += $updates
        RETURN p
        """
        updates = {k: v for k, v in {"name": name, "price": price}.items() if v is not None}
        with self.driver.session() as session:
            result = session.run(query, product_id=product_id, updates=updates)
            logging.info(f"Обновлены данные продукта с ID {product_id}: {updates}")
            return result.single()["p"]

    def delete_product(self, product_id):
        query = """
        MATCH (p:Product {product_id: $product_id})
        DETACH DELETE p
        """
        with self.driver.session() as session:
            session.run(query, product_id=product_id)
            logging.info(f"Удалён продукт с ID {product_id}")

    def create_category(self, category_id, category_name):
        query = """
        CREATE (c:Category {category_id: $category_id, category_name: $category_name})
        RETURN c
        """
        with self.driver.session() as session:
            result = session.run(query, category_id=category_id, category_name=category_name)
            logging.info(f"Создана категория с ID {category_id}, имя: {category_name}")
            return result.single()["c"]

    def get_category(self, category_id):
        query = """
        MATCH (c:Category {category_id: $category_id})
        RETURN c
        """
        with self.driver.session() as session:
            result = session.run(query, category_id=category_id)
            category = result.single()
            if category:
                logging.info(f"Найдена категория с ID {category_id}")
            else:
                logging.warning(f"Категория с ID {category_id} не найдена")
            return category["c"] if category else None

    def update_category(self, category_id, category_name):
        query = """
        MATCH (c:Category {category_id: $category_id})
        SET c.category_name = $category_name
        RETURN c
        """
        with self.driver.session() as session:
            result = session.run(query, category_id=category_id, category_name=category_name)
            logging.info(f"Обновлена категория с ID {category_id}, новое имя: {category_name}")
            return result.single()["c"]

    def delete_category(self, category_id):
        query = """
        MATCH (c:Category {category_id: $category_id})
        DETACH DELETE c
        """
        with self.driver.session() as session:
            session.run(query, category_id=category_id)
            logging.info(f"Удалена категория с ID {category_id}")

    def create_order_item(self, order_id, product_id):
        query = """
        MATCH (o:Order {order_id: $order_id}), (p:Product {product_id: $product_id})
        CREATE (o)-[:CONTAINS]->(p)
        """
        with self.driver.session() as session:
            session.run(query, order_id=order_id, product_id=product_id)
            logging.info(f"Добавлен продукт с ID {product_id} в заказ с ID {order_id}")

    def get_products_by_order_id(self, order_id):
        query = """
        MATCH (o:Order {order_id: $order_id})-[:CONTAINS]->(p:Product)
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, order_id=order_id)
            products = [record["p"] for record in result]
            logging.info(f"Найдены продукты для заказа с ID {order_id}: {len(products)} продуктов")
            return products

    def get_orders_by_user_id(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:PLACED]->(o:Order)
        RETURN o
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            orders = [record["o"] for record in result]
            logging.info(f"Найдены заказы для пользователя с ID {user_id}: {len(orders)} заказов")
            return orders

    def get_users_with_similar_purchases(self, user_id):
        query = """
        MATCH (u1:User {user_id: $user_id})-[:PLACED]->(:Order)-[:CONTAINS]->(p:Product)<-[:CONTAINS]-(:Order)<-[:PLACED]-(u2:User)
        WHERE u1 <> u2
        RETURN DISTINCT u2
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            users = [record["u2"] for record in result]
            logging.info(f"Найдены пользователи с похожими покупками для пользователя с ID {user_id}: {len(users)} пользователей")
            return users

    def get_products_by_category_id(self, category_id):
        query = """
        MATCH (p:Product)-[:BELONGS_TO]->(c:Category {category_id: $category_id})
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, category_id=category_id)
            products = [record["p"] for record in result]
            logging.info(f"Найдены продукты для категории с ID {category_id}: {len(products)} продуктов")
            return products