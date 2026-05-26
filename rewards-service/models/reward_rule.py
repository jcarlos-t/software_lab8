from dataclasses import dataclass


@dataclass(frozen=True)
class RewardRule:
    """Value Object: regla de cálculo de recompensas por restaurante."""

    restaurant_code: str
    points_per_unit: float = 1.0    # puntos por cada sol/dólar gastado
    cashback_rate: float = 0.02     # porcentaje de cashback (ej: 2%)

    def calculate_points(self, amount: float) -> float:
        return round(amount * self.points_per_unit, 2)

    def calculate_cashback(self, amount: float) -> float:
        return round(amount * self.cashback_rate, 2)
