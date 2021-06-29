from asyncpg import UniqueViolationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common import models
from common.logger import get_logger
from database.database import metadata, database, engine
from payment_service.app.api import (
    users_api_router,
    payments_api_router,
    payment_methods_api_router,
    user_payment_methods_api_router,
    currencies_api_router,
    ui_api_router,
)

logger = get_logger(__name__)

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Payment service starting up")
    await database.connect()
    await init_demo_records()
    logger.info("Bootstrapping payment service")


async def init_demo_records():
    from database import crud

    try:
        await crud.currencies.insert_currency(
            models.Currency(
                code="USD",
                name="US Dollar",
            )
        )
        await crud.currencies.insert_currency(
            models.Currency(
                code="EUR",
                name="Euro",
            ),
        )
        await crud.currencies.insert_currency(
            models.Currency(
                code="ILS",
                name="Israeli Shekel",
            )
        )

        await crud.payment_methods.insert_payment_method(
            models.PaymentMethod(
                guid="493f7c9b-8748-499c-b138-25f100ddf66a",
                name="Bank transfer",
            )
        )
        await crud.payment_methods.insert_payment_method(
            models.PaymentMethod(
                guid="27a58261-0f89-41b9-9c41-40ce4b53ec2f",
                name="Credit card",
            )
        )
        await crud.payment_methods.insert_payment_method(
            models.PaymentMethod(
                guid="1d9d87b0-1e19-40de-8299-45e4c3b3b325",
                name="Check",
            )
        )
        await crud.payment_methods.insert_payment_method(
            models.PaymentMethod(
                guid="10451c6e-ecb0-4114-b1f9-9f11e2e40a5a",
                name="Cash",
            )
        )

        await crud.users.insert_user(
            models.User(
                guid="b24312dc-53b8-4018-94ce-1e11d19887db",
                first_name="John",
                last_name="Doe",
                email_address="test@test.com",
            )
        )
        await crud.users.insert_user(
            models.User(
                guid="68b490b7-5341-47e0-99c6-7e84a61cbbf9",
                first_name="Johnny",
                last_name="Doe",
                email_address="test2@test.com",
            )
        )
        await crud.users.insert_user(
            models.User(
                guid="b7f9d6b4-6b62-4b83-a940-8502c9ab8b95",
                first_name="Johanna",
                last_name="Doe",
                email_address="test3@test.com",
            )
        )

        await crud.user_payment_methods.insert_user_payment_method(
            user_guid="b24312dc-53b8-4018-94ce-1e11d19887db",
            payment_method=models.PaymentMethod(
                guid="493f7c9b-8748-499c-b138-25f100ddf66a"
            ),
        )
        await crud.user_payment_methods.insert_user_payment_method(
            user_guid="b24312dc-53b8-4018-94ce-1e11d19887db",
            payment_method=models.PaymentMethod(
                guid="1d9d87b0-1e19-40de-8299-45e4c3b3b325"
            ),
        )

        await crud.user_payment_methods.insert_user_payment_method(
            user_guid="68b490b7-5341-47e0-99c6-7e84a61cbbf9",
            payment_method=models.PaymentMethod(
                guid="493f7c9b-8748-499c-b138-25f100ddf66a"
            ),
        )
        await crud.user_payment_methods.insert_user_payment_method(
            user_guid="68b490b7-5341-47e0-99c6-7e84a61cbbf9",
            payment_method=models.PaymentMethod(
                guid="27a58261-0f89-41b9-9c41-40ce4b53ec2f"
            ),
        )

        await crud.user_payment_methods.insert_user_payment_method(
            user_guid="b7f9d6b4-6b62-4b83-a940-8502c9ab8b95",
            payment_method=models.PaymentMethod(
                guid="493f7c9b-8748-499c-b138-25f100ddf66a"
            ),
        )
        await crud.user_payment_methods.insert_user_payment_method(
            user_guid="b7f9d6b4-6b62-4b83-a940-8502c9ab8b95",
            payment_method=models.PaymentMethod(
                guid="10451c6e-ecb0-4114-b1f9-9f11e2e40a5a"
            ),
        )
    except UniqueViolationError:
        return


@app.on_event("shutdown")
async def shutdown_event():
    metadata.drop_all()
    await database.disconnect()
    logger.info("Payment service shutting down")


app.include_router(
    ui_api_router,
    tags=["ui"],
)

app.include_router(
    users_api_router,
    prefix="/api/v1",
    tags=["users"],
)

app.include_router(
    payments_api_router,
    prefix="/api/v1",
    tags=["payments"],
)

app.include_router(
    user_payment_methods_api_router,
    prefix="/api/v1",
    tags=["user-payment-methods"],
)

app.include_router(
    payment_methods_api_router,
    prefix="/api/v1",
    tags=["payment-methods"],
)

app.include_router(
    currencies_api_router,
    prefix="/api/v1",
    tags=["currencies"],
)


if __name__ == "__main__":
    import uvicorn

    logger.debug("Running in debug")
    uvicorn.run(app, host="0.0.0.0", port=8080)
