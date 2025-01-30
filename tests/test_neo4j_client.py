
import pytest
from clients.neo4j_client import Neo4jClient

@pytest.fixture(scope="module")
def neo4j_client():
    client = Neo4jClient()
    yield client
    client.close()

@pytest.fixture(scope="module")
def setup_data(neo4j_client):
    client = neo4j_client

    client.create_user("user1", "Test User 1", "user1@example.com", "2024-01-01")
    client.create_user("user2", "Test User 2", "user2@example.com", "2024-01-02")

    client.create_category("cat1", "Test Category 1")
    client.create_category("cat2", "Test Category 2")

    client.create_product("prod1", "Test Product 1", 100, "cat1")
    client.create_product("prod2", "Test Product 2", 200, "cat1")
    client.create_product("prod3", "Test Product 3", 300, "cat2")

    client.create_order("order1", "2024-01-10", 300, "user1")
    client.create_order("order2", "2024-01-15", 500, "user1")
    client.create_order("order3", "2024-01-20", 700, "user2")

    client.create_order_item("order1", "prod1")
    client.create_order_item("order1", "prod2")
    client.create_order_item("order2", "prod3")
    client.create_order_item("order3", "prod1")
    client.create_order_item("order3", "prod2")

    yield

    # client.delete_user("user1")
    # client.delete_user("user2")
    # client.delete_category("cat1")
    # client.delete_category("cat2")
    # client.delete_product("prod1")
    # client.delete_product("prod2")
    # client.delete_product("prod3")
    # client.delete_order("order1")
    # client.delete_order("order2")
    # client.delete_order("order3")

def test_get_orders_by_user_id(neo4j_client, setup_data):
    orders = neo4j_client.get_orders_by_user_id("user1")
    order_ids = [order["order_id"] for order in orders]
    assert len(orders) == 2
    assert "order1" in order_ids
    assert "order2" in order_ids

def test_get_products_by_order_id(neo4j_client, setup_data):
    products = neo4j_client.get_products_by_order_id("order1")
    product_ids = [product["product_id"] for product in products]
    assert len(products) == 2
    assert "prod1" in product_ids
    assert "prod2" in product_ids

def test_get_users_with_similar_purchases(neo4j_client, setup_data):
    users = neo4j_client.get_users_with_similar_purchases("user1")
    user_ids = [user["user_id"] for user in users]
    assert len(users) == 1
    assert "user2" in user_ids

def test_get_products_by_category_id(neo4j_client, setup_data):
    products = neo4j_client.get_products_by_category_id("cat1")
    product_ids = [product["product_id"] for product in products]
    assert len(products) == 2
    assert "prod1" in product_ids
    assert "prod2" in product_ids
