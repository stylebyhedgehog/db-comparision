import pytest
from clients.postgresql_client import PostgreSQLClient


@pytest.fixture(scope="module")
def db_client():
    client = PostgreSQLClient()
    yield client
    client.connection.close()


@pytest.fixture(scope="module")
def setup_data(db_client):
    # Adding test users, products, orders, and order items to the database
    user_id = db_client.create_user("Test User", "test@example.com", "2024-12-20")
    category_id = db_client.create_category("Test Category")
    product_id_1 = db_client.create_product("Test Product 1", 100.0, category_id)
    product_id_2 = db_client.create_product("Test Product 2", 150.0, category_id)
    order_id = db_client.create_order(user_id, "2024-12-20", 250.0)

    db_client.create_order_item(order_id, product_id_1, 2)
    db_client.create_order_item(order_id, product_id_2, 1)

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
    assert orders[0][0] == setup_data["order_id"]


def test_get_products_by_user_id(db_client, setup_data):
    user_id = setup_data["user_id"]
    products = db_client.get_products_by_user_id(user_id)
    assert len(products) == 2
    product_ids = [product[0] for product in products]
    assert setup_data["product_id_1"] in product_ids
    assert setup_data["product_id_2"] in product_ids


def test_get_users_with_similar_purchases(db_client, setup_data):
    user_id = setup_data["user_id"]

    similar_user_id = db_client.create_user("Similar User", "similar@example.com", "2024-12-20")
    order_id = db_client.create_order(similar_user_id, "2024-12-20", 250.0)
    db_client.create_order_item(order_id, setup_data["product_id_1"], 2)
    db_client.create_order_item(order_id, setup_data["product_id_2"], 1)

    similar_users = db_client.get_users_with_similar_purchases(user_id)

    assert len(similar_users) > 0
    assert any(user[0] == similar_user_id for user in similar_users)


def test_get_products_by_category_id(db_client, setup_data):
    category_id = setup_data["category_id"]
    products = db_client.get_products_by_category_id(category_id)
    assert len(products) == 2
    product_ids = [product[0] for product in products]
    assert setup_data["product_id_1"] in product_ids
    assert setup_data["product_id_2"] in product_ids
