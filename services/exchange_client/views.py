from fastapi import APIRouter, status, Depends, HTTPException
from .crud import exchange_client
from .schemas import ExchangeClient

router = APIRouter(tags=["Exchange Client"], prefix="/exchange_client")


@router.get("/convert", response_model=ExchangeClient)
def convert(from_currency: str, to_currency: str, price: float):
    result = exchange_client.convert_price(
        from_curr=from_currency.upper(),
        to_curr=to_currency.upper(),
        price=price,
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось выполнить конвертацию.",
        )
    return {
        "price": price,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "result_convert": result,
    }
