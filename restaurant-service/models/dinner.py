from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class Dinner:
    """Entidad de dominio: representa una cena registrada en el restaurante."""

    dinner_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    amount: float = 0.0
    card_number: str = ""
    restaurant_code: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def validate(self) -> None:
        """Valida invariantes del dominio."""
        if self.amount <= 0:
            raise ValueError("El monto de la cena debe ser mayor a cero.")
        if not self.card_number:
            raise ValueError("El número de tarjeta no puede estar vacío.")
        if not self.restaurant_code:
            raise ValueError("El código del restaurante no puede estar vacío.")
