from .base import Base
from sqlalchemy import String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Product(Base):
    name: Mapped[str] = mapped_column(String(45))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="products")
