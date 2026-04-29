from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app
from services.users import views as users_views

client = TestClient(app)


def _override_user(user):
    async def _inner():
        return user

    return _inner


def test_login_user():
    user = SimpleNamespace(id=3, role="user")

    with (
        patch(
            "services.users.views.crud.authenticate_user",
            new=AsyncMock(return_value=user),
        ),
        patch("services.users.views.create_access_token", return_value="token-123"),
    ):
        response = client.post(
            "/users/login",
            data={"username": "user@example.com", "password": "secret"},
        )

    assert response.status_code == 200
    assert response.json()["access_token"] == "token-123"


def test_read_current_user():
    app.dependency_overrides[users_views.get_current_user] = _override_user(
        {
            "id": 1,
            "email": "user@example.com",
            "username": "user",
            "role": "user",
            "is_active": True,
            "is_verified": False,
        }
    )

    response = client.get("/users/me")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


@patch("services.products.crud.get_products_by_owner")
def test_get_user_products(mock_get_products_by_owner):
    mock_get_products_by_owner.return_value = [
        {
            "id": 2,
            "name": "Phone",
            "description": "Simple phone",
            "price": "5000.00",
            "owner_id": 2,
        }
    ]

    response = client.get("/products/test/2")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 2


def test_convert_currency():
    with patch(
        "services.exchange_client.views.exchange_client.convert_price",
        return_value=91.0,
    ):
        response = client.get(
            "/exchange_client/convert?from_currency=usd&to_currency=eur&price=100"
        )

    assert response.status_code == 200
    assert response.json()["result_convert"] == 91.0


def test_get_external_post():
    with patch(
        "services.external_posts.views.client.get_post",
        new=AsyncMock(
            return_value={
                "userId": 1,
                "id": 9,
                "title": "post title",
                "body": "post body",
            }
        ),
    ):
        response = client.get("/external-posts/9")

    assert response.status_code == 200
    assert response.json()["title"] == "post title"
