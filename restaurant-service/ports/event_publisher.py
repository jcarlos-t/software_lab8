from abc import ABC, abstractmethod
from shared.events.consumption_event import ConsumptionEvent


class EventPublisher(ABC):
    """Puerto de salida: contrato para publicar el evento de consumo."""

    @abstractmethod
    def publish_consumption(self, event: ConsumptionEvent) -> None:
        """Publica el evento de consumo hacia el broker de mensajería."""
        ...
