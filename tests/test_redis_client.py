import pytest
from clients.redis_client import RedisClient


@pytest.fixture
def redis_client():
    client = RedisClient()
    client.client.flushdb()
    return client


def test_get_orders_by_user_id(redis_client):
    redis_client.create_user("1", "Alice", "alice@example.com")
    redis_client.create_category("1", "Electronics")
    redis_client.create_product("1", "Laptop", "1200.00", "1")
    redis_client.create_order("1", "1", [{"product_id": "1", "quantity": 1}])

    orders = redis_client.get_orders_by_user_id("1")

    assert len(orders) == 1
    assert orders[0]["user_id"] == "1"
    assert "items" in orders[0]
    assert len(orders[0]["items"]) == 1
    assert orders[0]["items"][0]["product_id"] == "1"


def test_get_purchased_products_by_user_id(redis_client):
    redis_client.create_user("1", "Alice", "alice@example.com")
    redis_client.create_category("1", "Electronics")
    redis_client.create_product("1", "Laptop", "1200.00", "1")
    redis_client.create_order("1", "1", [{"product_id": "1", "quantity": 1}])

    products = redis_client.get_purchased_products_by_user_id("1")

    assert len(products) == 1
    assert products[0]["name"] == "Laptop"
    assert products[0]["price"] == "1200.00"


def test_get_users_with_similar_purchases(redis_client):
    redis_client.create_user("1", "Alice", "alice@example.com")
    redis_client.create_user("2", "Bob", "bob@example.com")
    redis_client.create_category("1", "Electronics")
    redis_client.create_product("1", "Laptop", "1200.00", "1")
    redis_client.create_product("2", "Smartphone", "800.00", "1")
    redis_client.create_order("1", "1", [{"product_id": "1", "quantity": 1}])
    redis_client.create_order("2", "2", [{"product_id": "1", "quantity": 1}, {"product_id": "2", "quantity": 1}])

    similar_users = redis_client.get_users_with_similar_purchases("1")

    assert len(similar_users) == 1
    assert similar_users[0]["name"] == "Bob"


def test_get_products_by_category_id(redis_client):
    redis_client.create_category("1", "Electronics")
    redis_client.create_product("1", "Laptop", "1200.00", "1")
    redis_client.create_product("2", "Smartphone", "800.00", "1")

    products = redis_client.get_products_by_category_id("1")

    assert len(products) == 2
    assert any(product["name"] == "Laptop" for product in products)
    assert any(product["name"] == "Smartphone" for product in products)
