from datetime import datetime

import aiohttp
from fastapi import FastAPI, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import FileResponse

from common.config import PAYMENTS_URI, ROOT_DIR
from payment_service.app.api.models import Payment

app = FastAPI()


@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse(f"{ROOT_DIR}/ui_service/app/static/index.html")


@app.post("/", status_code=201)
async def post_payment(
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

    async with aiohttp.ClientSession() as session:
        message = jsonable_encoder(payment)
        async with session.post(url=PAYMENTS_URI, json=message) as response:
            if response.status == 204:
                return {"payment": message}
            else:
                response_body = await response.text()
                return HTTPException(status_code=response.status, detail=response_body)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8011)
