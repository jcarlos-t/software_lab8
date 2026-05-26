from abc import ABC, abstractmethod
from models.dinner import Dinner


class DinnerRepository(ABC):
    """Puerto de salida: contrato para persistir cenas."""

    @abstractmethod
    def save(self, dinner: Dinner) -> None:
        """Guarda una cena en el repositorio."""
        ...

    @abstractmethod
    def find_by_id(self, dinner_id: str) -> Dinner | None:
        """Busca una cena por su ID."""
        ...
