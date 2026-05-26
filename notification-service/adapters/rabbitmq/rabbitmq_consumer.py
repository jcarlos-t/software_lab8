import json
import logging

import pika  # type: ignore

from services.send_notification import SendNotificationService
from adapters.senders.console_sender import ConsoleSender

logger = logging.getLogger(__name__)

NOTIFICATION_QUEUE = "notification_events"


class RabbitMQConsumer:
    """Adaptador de entrada: escucha eventos de notificación desde RabbitMQ."""

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
        self._connection = None
        self._channel = None

    def _build_service(self) -> SendNotificationService:
        return SendNotificationService(sender=ConsoleSender())

    def _on_message(self, channel, method, properties, body: bytes) -> None:
        try:
            data = json.loads(body)
            service = self._build_service()
            service.execute(
                card_number=data["card_number"],
                restaurant_code=data["restaurant_code"],
                amount=float(data["amount"]),
                points=float(data["points"]),
                cashback=float(data["cashback"]),
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:
            logger.error("Error procesando notificación: %s", exc)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start(self) -> None:
        credentials = pika.PlainCredentials(self._username, self._password)
        params = pika.ConnectionParameters(
            host=self._host, port=self._port, virtual_host=self._virtual_host, credentials=credentials
        )
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)
        self._channel.basic_consume(
            queue=NOTIFICATION_QUEUE, on_message_callback=self._on_message
        )
        logger.info("Notification consumer iniciado, esperando mensajes...")
        self._channel.start_consuming()

    def stop(self) -> None:
        if self._channel:
            self._channel.stop_consuming()
        if self._connection and not self._connection.is_closed:
            self._connection.close()
