from typing import List

from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from common.logger import get_logger
from database import crud
from payment_service.app.api.models import Currency

logger = get_logger(__name__)

currencies_api_router = APIRouter()


@currencies_api_router.post("/currencies", status_code=204)
async def post_currencies(currency: Currency):
    try:
        await crud.currencies.insert_currency(currency)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except UniqueViolationError:
        raise HTTPException(
            status_code=409, detail=f"Currency {currency} already exists"
        )


@currencies_api_router.get("/currencies", response_model=List[Currency])
async def get_currencies():
    return await crud.currencies.get_currencies()


@currencies_api_router.get("/currencies/{code}/", response_model=Currency)
async def get_currency_by_code(code: str):
    currency = await crud.currencies.get_currency_by_code(code=code)
    if currency is None:
        raise HTTPException(status_code=404, detail=f"Currency {code} not found")
    return currency
