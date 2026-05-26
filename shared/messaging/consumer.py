from abc import ABC, abstractmethod
from typing import Callable
from shared.events.consumption_event import ConsumptionEvent


class AbstractConsumer(ABC):
    """Puerto de entrada: contrato para consumir eventos del broker."""

    @abstractmethod
    def start(self, queue: str, handler: Callable[[ConsumptionEvent], None]) -> None:
        """Inicia la escucha de la cola indicada y llama a handler por cada mensaje."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Detiene la escucha."""
        ...
