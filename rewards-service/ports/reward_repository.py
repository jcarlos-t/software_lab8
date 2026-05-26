from abc import ABC, abstractmethod
from models.reward_account import RewardAccount


class RewardRepository(ABC):
    """Puerto de salida: contrato para persistir cuentas de recompensas."""

    @abstractmethod
    def find_by_card(self, card_number: str) -> RewardAccount | None:
        ...

    @abstractmethod
    def save(self, account: RewardAccount) -> None:
        ...
