import json
import logging

import pika  # type: ignore

from ports.notification_publisher import NotificationPublisher
from shared.events.consumption_event import ConsumptionEvent

logger = logging.getLogger(__name__)

NOTIFICATION_QUEUE = "notification_events"


class RabbitMQNotificationPublisher(NotificationPublisher):
    """Adaptador de salida: publica eventos de notificación en RabbitMQ."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def publish_reward_processed(
        self, event: ConsumptionEvent, points: float, cashback: float
    ) -> None:
        credentials = pika.PlainCredentials(self._username, self._password)
        params = pika.ConnectionParameters(host=self._host, port=self._port, credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)
        body = json.dumps({
            "card_number": event.card_number,
            "restaurant_code": event.restaurant_code,
            "amount": event.amount,
            "points": points,
            "cashback": cashback,
            "timestamp": event.timestamp.isoformat(),
        })
        channel.basic_publish(
            exchange="",
            routing_key=NOTIFICATION_QUEUE,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        logger.info("Evento de notificación publicado para: %s", event.card_number)
        connection.close()
