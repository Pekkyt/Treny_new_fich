from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .schemas import ProductCreate, ProductUpdate
from core.models.product import Product


async def create_product(
    session: AsyncSession,
    product_in: ProductCreate,
    owner_id: int,
) -> Product:
    product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        owner_id=owner_id,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def get_products_by_owner(
    session: AsyncSession,
    owner_id: int,
) -> list[Product]:
    stmt = select(Product).where(Product.owner_id == owner_id)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(
    session: AsyncSession,
    product_id: int,
) -> Product | None:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    return product


async def update_product(
    product_update: ProductUpdate,
    session: AsyncSession,
    product: Product,
) -> Product:
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()
