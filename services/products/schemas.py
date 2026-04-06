from pydantic import BaseModel
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    owner_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
