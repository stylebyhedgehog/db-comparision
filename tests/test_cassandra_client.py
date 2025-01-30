import pytest
import uuid
from clients.cassandra_client import CassandraClient

@pytest.fixture(scope="module")
def db_client():
    client = CassandraClient()
    yield client
    client.close()

@pytest.fixture(scope="module")
def setup_data(db_client):
    # Adding test users, products, orders, and order items to the database
    user_id = db_client.create_user("Test User", "test@example.com", "2024-12-20")
    category_id = uuid.uuid4()
    product_id_1 = uuid.uuid4()
    product_id_2 = uuid.uuid4()

    db_client.add_product_to_category(category_id, product_id_1, "Test Product 1", 100.0)
    db_client.add_product_to_category(category_id, product_id_2, "Test Product 2", 150.0)

    db_client.add_product_to_user(user_id, product_id_1, "Test Product 1", 100.0)
    db_client.add_product_to_user(user_id, product_id_2, "Test Product 2", 150.0)

    order_id = db_client.create_order(user_id, "2024-12-20", 250.0)

    db_client.create_order_item(order_id, product_id_1, "Test Product 1", 100.0, 2)
    db_client.create_order_item(order_id, product_id_2, "Test Product 2", 150.0, 1)

    return {
        "user_id": user_id,
        "category_id": category_id,
        "product_id_1": product_id_1,
        "product_id_2": product_id_2,
        "order_id": order_id
    }

def test_get_orders_by_user_id(db_client, setup_data):
    user_id = setup_data["user_id"]
    orders = db_client.get_orders_by_user_id(user_id)
    assert len(orders) == 1
    assert orders[0].order_id == setup_data["order_id"]

def test_get_products_by_user_id(db_client, setup_data):
    user_id = setup_data["user_id"]
    products = db_client.get_products_by_user_id(user_id)
    assert len(products) == 2
    product_ids = [product.product_id for product in products]
    assert setup_data["product_id_1"] in product_ids
    assert setup_data["product_id_2"] in product_ids

def test_get_users_with_similar_purchases(db_client, setup_data):
    user_id = setup_data["user_id"]

    similar_user_id = db_client.create_user("Similar User", "similar@example.com", "2024-12-20")
    db_client.add_product_to_user(similar_user_id, setup_data["product_id_1"], "Test Product 1", 100.0)
    db_client.add_product_to_user(similar_user_id, setup_data["product_id_2"], "Test Product 2", 150.0)

    similar_users = db_client.get_users_with_similar_purchases(user_id)

    assert len(similar_users) > 0
    assert similar_user_id in similar_users


def test_get_products_by_category_id(db_client, setup_data):
    category_id = setup_data["category_id"]
    products = db_client.get_products_by_category_id(category_id)
    assert len(products) == 2
    product_ids = [product.product_id for product in products]
    assert setup_data["product_id_1"] in product_ids
    assert setup_data["product_id_2"] in product_ids
