from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import ProductCreate, ProductRead, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper
from services.users.dependencies import get_current_user
from core.models.user import User
from . import crud
from core.models.product import Product
from .dependencies import (
    get_current_user_product,
    send_email_with_created_order,
    report_created_product,
)
from services.queue_producer import producer

router = APIRouter(tags=["PRODUCTS"], prefix="/products")

"""queue_task = queue.Queue()"""


@router.get("/my", response_model=list[ProductRead])
async def read_my_products(
    session: AsyncSession = Depends(db_helper.session_dependencies),
    current_user: User = Depends(get_current_user),
):
    products = await crud.get_products_by_owner(
        session=session, owner_id=current_user.id
    )
    return products


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_helper.session_dependencies),
    product: Product = Depends(get_current_user_product),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: AsyncSession = Depends(db_helper.session_dependencies),
    product: Product = Depends(get_current_user_product),
):
    await crud.delete_product(session=session, product=product)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_dependencies),
    current_user: User = Depends(get_current_user),
):
    product = await crud.create_product(
        session=session,
        product_in=product_in,
        owner_id=current_user.id,
    )

    # отправка задач через обычную очередь
    """queue_task.put(
        {
            "task": "send_email",
            "product_id": product.id,
            "user_email": current_user.email,
        }
    )
    queue_task.put(
        {
            "task": "report",
            "user_id": current_user.id,
            "product_id": product.id,
            "product_price": product.price,
        }
    )"""

    producer.send_product_task(
        task="send_email",
        product_id=product.id,
        data={"user_email": current_user.email},
    )
    producer.send_product_task(
        task="report",
        product_id=product.id,
        data={
            "user_id": current_user.id,
            "product_price": str(product.price),
        },
    )
    return product


"""def process_queue():
    while True:
        try:
            message = queue_task.get(timeout=1)
            task = message["task"]
            if task == "send_email":
                send_email_with_created_order(
                    message["user_email"], message["product_id"]
                )
            elif task == "report":
                report_created_product(
                    product_id=message["product_id"],
                    product_price=message["product_price"],
                    user_id=message["user_id"],
                )
            queue_task.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Ошибка обработки задачи: {e}")"""


@router.post("/orders/", status_code=status.HTTP_201_CREATED)
async def create_order():
    # данные из бд типо
    product_id = 3
    product_price = 1000
    user_id = 10
    email = "me@gmail.com"

    producer.send_product_task(
        task="send_email",
        product_id=product_id,
        data={"user_email": email},
    )
    producer.send_product_task(
        task="report",
        product_id=product_id,
        data={
            "user_id": user_id,
            "product_price": str(product_price),
        },
    )
    return {"product_id": product_id, "status_order": "created"}


@router.get("/test/{user_id}/", status_code=status.HTTP_200_OK)
async def get_user_products(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependencies),
):
    return await crud.get_products_by_owner(owner_id=user_id, session=session)
