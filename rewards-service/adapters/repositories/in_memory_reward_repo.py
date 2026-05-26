from models.reward_account import RewardAccount
from ports.reward_repository import RewardRepository


class InMemoryRewardRepository(RewardRepository):
    """Adaptador de salida: repositorio en memoria para cuentas de recompensas."""

    def __init__(self) -> None:
        self._store: dict[str, RewardAccount] = {}

    def find_by_card(self, card_number: str) -> RewardAccount | None:
        return self._store.get(card_number)

    def save(self, account: RewardAccount) -> None:
        self._store[account.card_number] = account

    @property
    def count(self) -> int:
        return len(self._store)
