from dataclasses import dataclass, field


@dataclass
class RewardAccount:
    """Entidad de dominio: cuenta de recompensas de un cliente."""

    card_number: str
    points_balance: float = 0.0
    cashback_balance: float = 0.0

    def add_points(self, points: float) -> None:
        if points < 0:
            raise ValueError("Los puntos a añadir no pueden ser negativos.")
        self.points_balance += points

    def add_cashback(self, cashback: float) -> None:
        if cashback < 0:
            raise ValueError("El cashback a añadir no puede ser negativo.")
        self.cashback_balance += cashback

    def total_value(self) -> float:
        """Retorna el valor total (puntos + cashback) de la cuenta."""
        return self.points_balance + self.cashback_balance
