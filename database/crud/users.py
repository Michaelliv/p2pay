from payment_service.app.api.models import User
from database.database import users_table, database


async def insert_user(user: User):
    query = users_table.insert().values(
        **user.dict(exclude_none=True, exclude_unset=True)
    )
    return await database.execute(query)


async def get_users():
    query = users_table.select()
    return await database.fetch_all(query=query)


async def get_user_by_guid(guid: str):
    query = users_table.select(users_table.columns.guid == guid)
    return await database.fetch_one(query=query)
