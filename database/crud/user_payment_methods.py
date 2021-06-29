from database.database import (
    user_payment_methods_table,
    database,
)
from payment_service.app.api.models import PaymentMethod


async def insert_user_payment_method(user_guid: str, payment_method: PaymentMethod):
    payment_method = payment_method.dict(exclude_none=True, exclude_unset=True)
    query = user_payment_methods_table.insert().values(
        user_guid=user_guid,
        payment_method_guid=payment_method.pop("guid"),
        **payment_method,
    )
    return await database.execute(query)


async def get_user_payment_methods(user_guid: str):
    query = f"""
    SELECT * FROM 
    (
        SELECT	user_guid,
                payment_method_guid,
                details
        FROM 	public.user_payment_methods
        WHERE 	user_guid = '{user_guid}'
    ) b
    LEFT JOIN
    (
        SELECT	guid as payment_method_guid, 
                name 
        FROM 	public.payment_methods
    ) g USING (payment_method_guid)

    """
    user_payment_methods = await database.fetch_all(query=query)
    return user_payment_methods
