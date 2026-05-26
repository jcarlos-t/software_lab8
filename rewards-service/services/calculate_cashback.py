from models.reward_rule import RewardRule


class CalculateCashbackService:
    """Caso de uso: calcular el cashback obtenido por una cena."""

    def execute(self, amount: float, restaurant_code: str) -> float:
        rule = RewardRule(restaurant_code=restaurant_code)
        return rule.calculate_cashback(amount)
