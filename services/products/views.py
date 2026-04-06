from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import ProductCreate, ProductRead, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.db_helper import db_helper
from services.users.dependencies import get_current_user
from core.models.user import User
from . import crud
from core.models.product import Product
from .dependencies import get_current_user_product

router = APIRouter(tags=["PRODUCTS"], prefix="/products")


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
    return product


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
