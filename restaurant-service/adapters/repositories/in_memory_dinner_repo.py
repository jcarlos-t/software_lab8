from models.dinner import Dinner
from ports.dinner_repository import DinnerRepository


class InMemoryDinnerRepository(DinnerRepository):
    """Adaptador de salida: repositorio en memoria (para pruebas)."""

    def __init__(self) -> None:
        self._store: dict[str, Dinner] = {}

    def save(self, dinner: Dinner) -> None:
        self._store[dinner.dinner_id] = dinner

    def find_by_id(self, dinner_id: str) -> Dinner | None:
        return self._store.get(dinner_id)

    @property
    def count(self) -> int:
        return len(self._store)
