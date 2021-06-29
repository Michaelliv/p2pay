from common.models import PaymentMethod
from database.database import payment_methods_table, database


async def insert_payment_method(payment_method: PaymentMethod):
    query = payment_methods_table.insert().values(
        **payment_method.dict(exclude_none=True, exclude_unset=True)
    )
    return await database.execute(query)


async def get_payment_methods():
    query = payment_methods_table.select()
    return await database.fetch_all(query=query)


async def get_payment_method_by_guid(guid: str):
    query = payment_methods_table.select(payment_methods_table.columns.guid == guid)
    return await database.fetch_one(query=query)
