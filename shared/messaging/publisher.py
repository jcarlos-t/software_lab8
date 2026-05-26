from abc import ABC, abstractmethod
from shared.events.consumption_event import ConsumptionEvent


class AbstractPublisher(ABC):
    """Puerto de salida: contrato para publicar eventos al broker."""

    @abstractmethod
    def publish(self, queue: str, event: ConsumptionEvent) -> None:
        """Publica un evento en la cola/tópico indicado."""
        ...
