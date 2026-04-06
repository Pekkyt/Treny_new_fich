from datetime import datetime
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class User(Base):
    username: Mapped[str] = mapped_column(String(45))
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(String(30), server_default="user")
    is_active: Mapped[bool] = mapped_column(server_default="true")
    is_verified: Mapped[bool] = mapped_column(server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    products: Mapped[list["Product"]] = relationship(back_populates="user")
