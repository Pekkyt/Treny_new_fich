from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException, Path
from core.models import Product
from core.models.user import User
from core.models.db_helper import db_helper
from . import crud
from services.users.dependencies import get_current_user


async def get_current_user_product(
    product_id: int = Path(...),
    session: AsyncSession = Depends(db_helper.session_dependencies),
    current_user: User = Depends(get_current_user),
) -> Product:
    product = await crud.get_product_by_id(
        session=session,
        product_id=product_id,
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this product",
        )
    return product


def send_email_with_created_order(
    user_email: str,
    product_id: int,
):
    print(
        f"Письмо о создании продукта {product_id} было отправлено на почту {user_email}"
    )


def report_created_product(product_id: int, product_price: int, user_id: int):
    print(
        f"Заказ {product_id} на сумму {product_price} руб. был создан пользователем {user_id}"
    )
