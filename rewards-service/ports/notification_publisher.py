from abc import ABC, abstractmethod
from shared.events.consumption_event import ConsumptionEvent


class NotificationPublisher(ABC):
    """Puerto de salida: publica evento para que el servicio de notificaciones actúe."""

    @abstractmethod
    def publish_reward_processed(self, event: ConsumptionEvent, points: float, cashback: float) -> None:
        ...
