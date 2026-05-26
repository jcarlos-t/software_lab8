"""Entry point del Notification Service."""

import logging
import os

from adapters.rabbitmq.rabbitmq_consumer import RabbitMQConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

if __name__ == "__main__":
    consumer = RabbitMQConsumer(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        username=os.getenv("RABBITMQ_USER", "guest"),
        password=os.getenv("RABBITMQ_PASS", "guest"),
    )
    consumer.start()
