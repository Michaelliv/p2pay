from typing import List

from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from common.logger import get_logger
from database import crud
from payment_service.app.api.models import PaymentMethod

logger = get_logger(__name__)

payment_methods_api_router = APIRouter()


@payment_methods_api_router.post("/paymentmethods", status_code=204)
async def post_payment_methods(payment_method: PaymentMethod):
    try:
        await crud.payment_methods.insert_payment_method(payment_method)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except UniqueViolationError:
        raise HTTPException(
            status_code=409, detail=f"Payment method {payment_method} already exists"
        )


@payment_methods_api_router.get("/paymentmethods", response_model=List[PaymentMethod])
async def get_payment_methods():
    return await crud.payment_methods.get_payment_methods()


@payment_methods_api_router.get("/paymentmethods/{guid}/", response_model=PaymentMethod)
async def get_payment_method_by_guid(guid: str):
    payment_method = await crud.payment_methods.get_payment_method_by_guid(guid=guid)
    if payment_method is None:
        raise HTTPException(status_code=404, detail=f"Payment method {guid} not found")
    return payment_method
