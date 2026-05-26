"""Entry point del Rewards Service."""

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
        port=int(os.getenv("RABBITMQ_PORT")),
        username=os.getenv("RABBITMQ_USER"),
        password=os.getenv("RABBITMQ_PASS"),
        virtual_host=os.getenv("RABBITMQ_VHOST"),
    )
    consumer.start()
