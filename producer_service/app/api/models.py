from datetime import datetime

from pydantic import BaseModel, validator


class ProducerResponse(BaseModel):
    payload_id: str
    topic: str
    timestamp: datetime = None

    @validator("timestamp", pre=True, always=True)
    def set_utc_timestamp(cls, v):
        return v or datetime.utcnow()
