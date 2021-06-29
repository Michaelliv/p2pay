from fastapi.encoders import jsonable_encoder

from common.logger import get_logger
from common.models import ProcessedPayment
from database.database import payments_table, database

logger = get_logger(__file__)


async def insert_processed_payment(processed_payment: ProcessedPayment):
    # Flatten model structure and insert to DB
    try:
        logger.info(
            f"Inserting processed payment [{processed_payment.transaction_guid}]..."
        )
        # Encode model values to serializable types
        encoded = jsonable_encoder(
            processed_payment.dict(exclude_none=True, exclude_unset=True),
        )
        query = payments_table.insert().values(encoded)
        await database.execute(query)
    except Exception as e:
        logger.exception(str(e))
        raise e


async def get_payments():
    logger.info("Getting payments...")
    query = payments_table.select()
    return await database.fetch_all(query=query)


async def get_payment_by_transaction_guid(guid: str):
    logger.info(f"Getting payment by transaction guid ({guid})...")
    query = payments_table.select(payments_table.columns.transaction_guid == guid)
    return await database.fetch_one(query=query)


async def get_payments_by_user_guid(guid: str):
    logger.info(f"Getting payments by user guid ({guid})...")
    query = payments_table.select(payments_table.columns.user_guid == guid)
    return await database.fetch_all(query=query)


async def get_payments_by_payee_guid(guid: str):
    logger.info(f"Getting payments by payee guid ({guid})...")
    query = payments_table.select(payments_table.columns.user_guid == guid)
    return await database.fetch_all(query=query)
