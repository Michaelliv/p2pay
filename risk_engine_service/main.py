import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

from aiokafka import AIOKafkaConsumer

import database.crud.payments as payments_crud
from common.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC
from common.logger import get_logger
from database.database import database
from risk_engine_service.engine import RandomRiskEngine, AbstractRiskEngine

logger = get_logger(__name__)


def init_stream_consumer() -> AIOKafkaConsumer:
    """ Initializes and returns the stream consumer """
    logger.info("Initializing stream consumer...")
    return AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        auto_offset_reset="earliest",
        auto_commit_interval_ms=1000,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )


def init_risk_engine() -> AbstractRiskEngine:
    """ Initializes and returns the risk engine """
    logger.info("Initializing risk engine...")
    return RandomRiskEngine(
        min_value=0.0,
        max_value=1.0,
        approval_threshold=0.7,
    )


async def main():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)

    risk_engine = init_risk_engine()
    consumer = init_stream_consumer()

    # Establish database connection and start consumer
    await database.connect()
    await consumer.start()

    try:
        logger.info("Consuming messages...")
        # Then processes them using the risk engine
        async for message in consumer:
            processed_payment = await loop.run_in_executor(
                executor, risk_engine.process, message.value
            )
            # Insert processed payment to database
            await payments_crud.insert_processed_payment(
                processed_payment=processed_payment
            )

    finally:
        logger.info("Stopping consumer and disconnecting from database gracefully...")
        await consumer.stop()
        await database.disconnect()


if __name__ == "__main__":
    """
    This is the entry point to the RiskEngine service, this service consumes a Kafka stream, applies the RiskEngine
    logic and writes its processed results to a database.

    This service handles 2 different types of workload:
    1) CPU/GPU bound RiskEngine (Basically non IO related work)
    2) IO bound writing results to DB

    We will start an event loop in its own thread and offload the second type of workload to this thread
    """
    asyncio.run(main())
