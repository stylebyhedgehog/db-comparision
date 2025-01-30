import os

from cassandra.cluster import Cluster
import uuid


class CassandraClient:

    def __init__(self):
        contact_points = os.getenv("CASSANDRA_CONTACT_POINTS", "localhost").split(",")
        port = int(os.getenv("CASSANDRA_PORT", 9042))
        keyspace = os.getenv("CASSANDRA_KEYSPACE", "test_keyspace")
        self.cluster = Cluster(contact_points, port=port)
        self.session = self.cluster.connect()
        self._initialize_keyspace_and_tables(keyspace)
        self.session.set_keyspace(keyspace)

    def _initialize_keyspace_and_tables(self, keyspace: str):
        self.session.execute(f"""
           CREATE KEYSPACE IF NOT EXISTS {keyspace}
           WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
           """)

        self.session.set_keyspace(keyspace)

        self.session.execute("""
           CREATE TABLE IF NOT EXISTS users (
               user_id UUID PRIMARY KEY,
               name TEXT,
               email TEXT,
               registration_date DATE
           );
           """)

        self.session.execute("""
           CREATE TABLE IF NOT EXISTS orders_by_user (
               user_id UUID,
               order_id UUID,
               order_date DATE,
               total DECIMAL,
               PRIMARY KEY (user_id, order_date, order_id)
           ) WITH CLUSTERING ORDER BY (order_date DESC);
           """)

        self.session.execute("""
           CREATE TABLE IF NOT EXISTS order_items_by_order (
               order_id UUID,
               product_id UUID,
               product_name TEXT,
               price DECIMAL,
               quantity INT,
               PRIMARY KEY (order_id, product_id)
           );
           """)

        self.session.execute("""
           CREATE TABLE IF NOT EXISTS products_by_category (
               category_id UUID,
               product_id UUID,
               product_name TEXT,
               price DECIMAL,
               PRIMARY KEY (category_id, product_id)
           );
           """)

        self.session.execute("""
           CREATE TABLE IF NOT EXISTS products_by_user (
               user_id UUID,
               product_id UUID,
               product_name TEXT,
               price DECIMAL,
               PRIMARY KEY (user_id, product_id)
           );
           """)

    def create_user(self, name, email, registration_date):
        user_id = uuid.uuid4()
        query = """
        INSERT INTO users (user_id, name, email, registration_date)
        VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (user_id, name, email, registration_date))
        return user_id

    def create_order(self, user_id, order_date, total):
        order_id = uuid.uuid4()
        query = """
        INSERT INTO orders_by_user (user_id, order_id, order_date, total)
        VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (user_id, order_id, order_date, total))
        return order_id

    def create_order_item(self, order_id, product_id, product_name, price, quantity):
        query = """
        INSERT INTO order_items_by_order (order_id, product_id, product_name, price, quantity)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.session.execute(query, (order_id, product_id, product_name, price, quantity))

    def add_product_to_category(self, category_id, product_id, product_name, price):
        query = """
        INSERT INTO products_by_category (category_id, product_id, product_name, price)
        VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (category_id, product_id, product_name, price))

    def add_product_to_user(self, user_id, product_id, product_name, price):
        query = """
        INSERT INTO products_by_user (user_id, product_id, product_name, price)
        VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (user_id, product_id, product_name, price))

    def get_orders_by_user_id(self, user_id):
        query = """
        SELECT * FROM orders_by_user WHERE user_id = %s
        """
        rows = self.session.execute(query, (user_id,))
        return list(rows)

    def get_products_by_user_id(self, user_id):
        query = """
        SELECT * FROM products_by_user WHERE user_id = %s
        """
        rows = self.session.execute(query, (user_id,))
        return list(rows)

    def get_users_with_similar_purchases(self, user_id):
        query = """
        SELECT product_id FROM products_by_user WHERE user_id = %s
        """
        purchased_products = [row.product_id for row in self.session.execute(query, (user_id,))]

        if not purchased_products:
            return []

        similar_users = set()

        for product_id in purchased_products:
            query = """
            SELECT user_id FROM products_by_user WHERE product_id = %s ALLOW FILTERING
            """
            rows = self.session.execute(query, (product_id,))
            for row in rows:
                if row.user_id != user_id:
                    similar_users.add(row.user_id)

        return list(similar_users)

    def get_products_by_category_id(self, category_id):
        query = """
        SELECT * FROM products_by_category WHERE category_id = %s
        """
        rows = self.session.execute(query, (category_id,))
        return list(rows)

    def close(self):
        self.cluster.shutdown()
