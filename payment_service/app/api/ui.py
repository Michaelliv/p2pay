from datetime import datetime

from fastapi import Form, APIRouter
from starlette.responses import FileResponse

from common.config import ROOT_DIR
from common.logger import get_logger
from common.models import Payment
from payment_service.app.api.payments import post_payment_to_producer

logger = get_logger(__name__)

ui_api_router = APIRouter()


@ui_api_router.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse(f"{ROOT_DIR}/payment_service/app/static/index.html")


@ui_api_router.post("/", status_code=204)
async def form_submit(
    from_field: str = Form(...),
    to_field: str = Form(...),
    currency: str = Form(...),
    payment_method: str = Form(...),
    sum: float = Form(...),
):
    payment = Payment(
        timestamp=datetime.utcnow(),
        user_guid=from_field,
        payee_guid=to_field,
        currency=currency,
        amount=sum,
        payment_method=payment_method,
    )

    response = await post_payment_to_producer(payment=payment)
    logger.debug(f"Payment sent to producer successfully {payment}")
    return response
