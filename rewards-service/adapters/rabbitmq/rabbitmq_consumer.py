import json
import logging
import threading

import pika  # type: ignore

from services.process_reward import ProcessRewardService
from adapters.repositories.in_memory_reward_repo import InMemoryRewardRepository
from adapters.repositories.rabbitmq_notification_publisher import RabbitMQNotificationPublisher
from shared.events.consumption_event import ConsumptionEvent

logger = logging.getLogger(__name__)

QUEUE_NAME = "consumption_events"


class RabbitMQConsumer:
    """Adaptador de entrada: escucha eventos de consumo desde RabbitMQ."""

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
        self._connection: pika.BlockingConnection | None = None
        self._channel = None

    def _build_service(self) -> ProcessRewardService:
        return ProcessRewardService(
            reward_repository=InMemoryRewardRepository(),
            notification_publisher=RabbitMQNotificationPublisher(
                host=self._host, port=self._port,
                username=self._username, password=self._password,
            ),
        )

    def _on_message(self, channel, method, properties, body: bytes) -> None:
        try:
            data = json.loads(body)
            event = ConsumptionEvent.from_dict(data)
            service = self._build_service()
            account = service.execute(event)
            logger.info(
                "Recompensa procesada para %s: puntos=%.2f cashback=%.2f",
                account.card_number, account.points_balance, account.cashback_balance,
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:  # noqa: BLE001
            logger.error("Error al procesar mensaje: %s", exc)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start(self) -> None:
        credentials = pika.PlainCredentials(self._username, self._password)
        params = pika.ConnectionParameters(host=self._host, port=self._port, credentials=credentials)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=QUEUE_NAME, durable=True)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=QUEUE_NAME, on_message_callback=self._on_message)
        logger.info("Rewards consumer iniciado, esperando mensajes en '%s'...", QUEUE_NAME)
        self._channel.start_consuming()

    def stop(self) -> None:
        if self._channel:
            self._channel.stop_consuming()
        if self._connection and not self._connection.is_closed:
            self._connection.close()
