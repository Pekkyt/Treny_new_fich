from decimal import Decimal

import pytest
from pydantic import ValidationError

from core.models.product import Product
from core.models.user import User
from services.work_with_backtasks.schemas import OrderCreate


@pytest.fixture
def order_data():
    return {
        "user_email": "user@example.com",
        "items": [{"product_id": 1, "qty": 2}],
        "total": 1500.0,
    }


@pytest.mark.parametrize(
    "model_class,expected_table",
    [
        (User, "user"),
        (Product, "product"),
    ],
)
def test_model_table_names(model_class, expected_table):
    assert model_class.__tablename__ == expected_table


def test_user_model_create():
    user = User(
        username="rodion",
        email="rodion@example.com",
        hashed_password="hashed-password",
    )

    assert user.username == "rodion"
    assert user.email == "rodion@example.com"
    assert user.hashed_password == "hashed-password"


def test_product_model_create():
    product = Product(
        name="Phone",
        description="Simple phone",
        price=Decimal("499.99"),
        owner_id=1,
    )

    assert product.name == "Phone"
    assert product.description == "Simple phone"
    assert product.price == Decimal("499.99")
    assert product.owner_id == 1


def test_order_schema_create(order_data):
    order = OrderCreate(**order_data)

    assert order.user_email == "user@example.com"
    assert order.items[0]["product_id"] == 1
    assert order.total == 1500.0


def test_order_schema_without_email_raises_error(order_data):
    order_data.pop("user_email")

    with pytest.raises(ValidationError):
        OrderCreate(**order_data)

