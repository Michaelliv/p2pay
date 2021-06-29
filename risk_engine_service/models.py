from pydantic import BaseModel

from payment_service.app.api.models import Payment


class ProcessedPayment(BaseModel):
    payment: Payment
    risk_score: float
    is_approved: bool
