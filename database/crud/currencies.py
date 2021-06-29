from payment_service.app.api.models import Currency
from database.database import currencies_table, database


async def insert_currency(currency: Currency):
    query = currencies_table.insert().values(
        **currency.dict(exclude_none=True, exclude_unset=True)
    )
    return await database.execute(query)


async def get_currencies():
    query = currencies_table.select()
    return await database.fetch_all(query=query)


async def get_currency_by_code(code: str):
    query = currencies_table.select(currencies_table.columns.code == code)
    return await database.fetch_one(query=query)
