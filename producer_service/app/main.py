import json
from typing import Optional

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from common.config import PROJECT_NAME, KAFKA_BOOTSTRAP_SERVERS
from common.logger import get_logger
from common.models import Payment

logger = get_logger(__name__)

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")

aio_producer: Optional[AIOKafkaProducer] = None


async def init_aio_kafka_producer():
    global aio_producer
    aio_producer = AIOKafkaProducer(
        client_id=PROJECT_NAME, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )


@app.on_event("startup")
async def startup_event():
    await init_aio_kafka_producer()
    await aio_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aio_producer.stop()


@app.post("/api/v1/producer/{topic}", status_code=204)
async def kafka_produce(topic: str, payment: Payment):
    try:
        await aio_producer.send(
            topic, json.dumps(jsonable_encoder(payment)).encode("ascii")
        )
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8091)
