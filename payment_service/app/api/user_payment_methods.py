from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from common.logger import get_logger
from database import crud
from payment_service.app.api.models import PaymentMethod, UserPaymentMethods

logger = get_logger(__name__)

user_payment_methods_api_router = APIRouter()


@user_payment_methods_api_router.post("/users/{guid}/paymentmethods", status_code=201)
async def post_user_payment_methods(guid: str, payment_method: PaymentMethod):
    try:
        await crud.user_payment_methods.insert_user_payment_method(
            user_guid=guid, payment_method=payment_method
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except UniqueViolationError:
        raise HTTPException(
            status_code=409,
            detail=f"Payment method {payment_method} for user {guid} already exists",
        )


@user_payment_methods_api_router.get(
    "/users/{guid}/paymentmethods", response_model=UserPaymentMethods
)
async def get_user_payment_methods_by_guid(guid: str):
    user_payment_methods = await crud.user_payment_methods.get_user_payment_methods(
        user_guid=guid
    )
    if not user_payment_methods:
        raise HTTPException(
            status_code=404, detail=f"Payment methods for user {guid} not found"
        )
    user_payment_methods_response = {"user_guid": "", "payment_methods": []}
    for user_payment_method in user_payment_methods:
        if not user_payment_methods_response["user_guid"]:
            user_payment_methods_response["user_guid"] = user_payment_method[
                "user_guid"
            ]
        user_payment_methods_response["payment_methods"].append(
            {
                "guid": user_payment_method["payment_method_guid"],
                "name": user_payment_method["name"],
                "details": user_payment_method["details"],
            }
        )
    return user_payment_methods_response
