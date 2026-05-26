from models.reward_rule import RewardRule


class CalculatePointsService:
    """Caso de uso: calcular los puntos obtenidos por una cena."""

    def execute(self, amount: float, restaurant_code: str) -> float:
        """
        Aplica la regla del restaurante y retorna los puntos calculados.

        Args:
            amount: monto de la cena.
            restaurant_code: código del restaurante.
        Returns:
            Puntos ganados.
        """
        rule = RewardRule(restaurant_code=restaurant_code)
        return rule.calculate_points(amount)
