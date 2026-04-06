from pydantic import BaseModel


class ExchangeClient(BaseModel):
    price: float
    from_currency: str
    to_currency: str
    result_convert: float
