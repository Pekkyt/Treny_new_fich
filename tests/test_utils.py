import pytest


@pytest.fixture
def product():
    return {
        "product_id": 1,
        "name": "Test Product",
        "description": "Test Product Description",
        "price": 5000,
    }


@pytest.fixture
def base_price():
    return 700


def test_without_discount(base_price):
    from utils.utils_function_for_tests import calculate_discount

    assert calculate_discount(base_price) == 0


@pytest.mark.parametrize(
    "order_total,expected_discount",
    [
        (500, 0),
        (1000, 50),
        (1500, 75),
        (5000, 500),
        (10000, 1500),
    ],
)
def test_calculate_discount(order_total, expected_discount):
    from utils.utils_function_for_tests import calculate_discount

    assert calculate_discount(order_total) == expected_discount


def test_price_product(product):
    assert product["price"] == 5000


def test_name_product(product):
    assert product["name"] == "Test Product"


def test_calculate_delivery():
    from utils.calculations import calculate_delivery

    result = calculate_delivery(
        weight=5,
        distance=50,
    )
    assert result == 400


@pytest.mark.parametrize(
    "weight,distance,expected_price",
    [
        (1, 10, 160),
        (5, 50, 400),
        (10, 100, 700),
    ],
)
def test_calculate_price(weight, distance, expected_price):
    from utils.calculations import calculate_delivery

    assert calculate_delivery(weight, distance) == expected_price
