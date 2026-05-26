from dataclasses import dataclass


@dataclass
class Notification:
    """Entidad de dominio: representa una notificación enviada al cliente."""

    card_number: str
    restaurant_code: str
    amount: float
    points: float
    cashback: float
    message: str = ""

    def build_message(self) -> str:
        self.message = (
            f"¡Hola! Tienes una nueva recompensa:\n"
            f"  Restaurante: {self.restaurant_code}\n"
            f"  Consumo:     S/ {self.amount:.2f}\n"
            f"  Puntos:      {self.points:.2f}\n"
            f"  Cashback:    S/ {self.cashback:.2f}\n"
        )
        return self.message
