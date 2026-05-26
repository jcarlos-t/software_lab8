import json
import logging

import pika  # type: ignore

from ports.event_publisher import EventPublisher
from shared.events.consumption_event import ConsumptionEvent

logger = logging.getLogger(__name__)

QUEUE_NAME = "consumption_events"


class RabbitMQEventPublisher(EventPublisher):
    """Adaptador de salida: publica eventos en RabbitMQ."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        virtual_host: str = "/",
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._virtual_host = virtual_host

    def _connect(self) -> tuple[pika.BlockingConnection, pika.channel.Channel]:
        credentials = pika.PlainCredentials(self._username, self._password)
        params = pika.ConnectionParameters(
            host=self._host, port=self._port, virtual_host=self._virtual_host, credentials=credentials
        )
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        return connection, channel

    def publish_consumption(self, event: ConsumptionEvent) -> None:
        connection, channel = self._connect()
        try:
            body = json.dumps(event.to_dict())
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),  # persistent
            )
            logger.info("Evento publicado: %s", event.event_id)
        finally:
            connection.close()
