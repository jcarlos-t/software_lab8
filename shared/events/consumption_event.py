from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass(frozen=True)
class ConsumptionEvent:
    """Evento publicado por el restaurante al broker cuando se registra una cena."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    amount: float = 0.0
    card_number: str = ""
    restaurant_code: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "amount": self.amount,
            "card_number": self.card_number,
            "restaurant_code": self.restaurant_code,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConsumptionEvent":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            amount=float(data["amount"]),
            card_number=data["card_number"],
            restaurant_code=data["restaurant_code"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
