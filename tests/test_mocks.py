from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from utils.calculations import calculate_delivery

client = TestClient(app)


@patch("utils.calculations.external_module.get_base_delivery_price")
def test_calculate_price(mock_get_base_delivery_price):
    mock_get_base_delivery_price.return_value = 100
    result = calculate_delivery(5, 50)
    assert result == 400
    mock_get_base_delivery_price.assert_called_once()


@patch("services.products.crud.get_products_by_owner")
def test_get_products_by_owner(mock_get_products_by_owner):
    mock_get_products_by_owner.return_value = [
        {
            "id": 2,
            "name": "Телевизор",
            "description": "120 кадров",
            "price": "5000.00",
            "owner_id": 2,
        },
        {
            "id": 4,
            "name": "Телефон",
            "description": "лучший",
            "price": "100000.00",
            "owner_id": 2,
        },
        {
            "id": 5,
            "name": "Гаджет",
            "description": "новый",
            "price": "1900.00",
            "owner_id": 2,
        },
        {
            "id": 6,
            "name": "Клей",
            "description": "жоский",
            "price": "200.00",
            "owner_id": 2,
        },
        {
            "id": 7,
            "name": "Ноутбук",
            "description": "классный 2026 года",
            "price": "120000.00",
            "owner_id": 2,
        },
        {
            "id": 8,
            "name": "Проверка",
            "description": "прошло или нет",
            "price": "1232.00",
            "owner_id": 2,
        },
        {
            "id": 9,
            "name": "еще одна",
            "description": "прошло или нет",
            "price": "12121212.00",
            "owner_id": 2,
        },
        {
            "id": 10,
            "name": "string",
            "description": "string",
            "price": "0.00",
            "owner_id": 2,
        },
    ]
    response = client.get("/products/test/2")
    assert response.status_code == 200
    assert len(response.json()) == 8
    assert response.json()[0]["id"] == 2
    mock_get_products_by_owner.assert_called_once()
