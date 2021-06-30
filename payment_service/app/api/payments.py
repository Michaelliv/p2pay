from typing import List, Union

import aiohttp
from fastapi import APIRouter, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_204_NO_CONTENT

from common.config import PRODUCER_URI
from common.logger import get_logger
from common.models import Payment
from database import crud

logger = get_logger(__name__)

payments_api_router = APIRouter()


@payments_api_router.post("/payments", status_code=204)
async def post_payment(payment: Payment):
    return await post_payment_to_producer(payment=payment)


async def post_payment_to_producer(payment: Payment) -> Response:
    async with aiohttp.ClientSession() as session:
        # We need to encode the payment model since datetime is not a serializable object
        message = jsonable_encoder(payment)
        async with session.post(url=PRODUCER_URI, json=message) as response:
            # Here we just assume everything is fine downstream, in real world scenario we would have liked to know
            # if anything went wrong
            if response.status == 204:
                return Response(status_code=HTTP_204_NO_CONTENT)
            else:
                response_body = await response.text()
                raise HTTPException(status_code=response.status, detail=response_body)


@payments_api_router.get("/payments", response_model=List[Payment])
async def get_payments():
    payments = await crud.payments.get_payments()
    return payments


@payments_api_router.get("/payments/{guid}/", response_model=Payment)
async def get_payments_by_guid(guid: str):
    return await crud.payments.get_payment_by_transaction_guid(guid)


@payments_api_router.get("/users/{guid}/payments", response_model=List[Payment])
async def get_payments_by_user_guid(guid: str):
    return await crud.payments.get_payments_by_user_guid(guid)
