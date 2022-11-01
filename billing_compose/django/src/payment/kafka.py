from functools import lru_cache
from typing import Optional

from config import settings
from kafka import KafkaProducer

kafka_producer: Optional[KafkaProducer] = None


def init_kafka_producer():
    global kafka_producer
    kafka_producer = KafkaProducer(
        bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
        api_version=(0, 11, 5),
    )
    return None


@lru_cache()
def get_kafka_producer():
    return kafka_producer
