import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator

"""
This module is used for creating Pydantic models that correspond a single row in DB tables
"""


class PaymentMethod(BaseModel):
    guid: str
    name: Optional[str] = None
    details: Optional[str] = None


class UserPaymentMethods(BaseModel):
    user_guid: str
    payment_methods: List[PaymentMethod]


class Currency(BaseModel):
    code: str
    name: str


class User(BaseModel):
    guid: str
    first_name: str
    last_name: str
    email_address: str


class Payment(BaseModel):
    timestamp: datetime
    user_guid: str
    payee_guid: str
    currency: str
    amount: float
    payment_method: str
    transaction_guid: Optional[str] = None

    @validator("transaction_guid", pre=True, always=True)
    def set_transaction_guid(cls, v):
        return str(uuid.uuid4())

    @validator("timestamp", pre=True, always=True)
    def set_utc_timestamp(cls, v):
        return v or datetime.utcnow()


class ProcessedPayment(Payment):
    risk_score: float
    is_approved: bool
