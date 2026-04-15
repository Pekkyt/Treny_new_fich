from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_email: str
    items: list[dict]
    total: float
