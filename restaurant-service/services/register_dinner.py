from dataclasses import dataclass
from datetime import datetime

from models.dinner import Dinner
from ports.dinner_repository import DinnerRepository
from ports.event_publisher import EventPublisher
from shared.events.consumption_event import ConsumptionEvent


@dataclass
class RegisterDinnerCommand:
    """Comando de entrada para registrar una nueva cena."""

    amount: float
    card_number: str
    restaurant_code: str
    timestamp: datetime | None = None


class RegisterDinnerService:
    """Caso de uso: Registrar Cena y publicar el evento de consumo."""

    def __init__(
        self,
        dinner_repository: DinnerRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self._dinner_repository = dinner_repository
        self._event_publisher = event_publisher

    def execute(self, command: RegisterDinnerCommand) -> Dinner:
        """
        Registra la cena, la persiste y publica el evento de consumo.

        Returns:
            La cena creada y persistida.
        Raises:
            ValueError: si los datos del comando son inválidos.
        """
        dinner = Dinner(
            amount=command.amount,
            card_number=command.card_number,
            restaurant_code=command.restaurant_code,
            timestamp=command.timestamp or datetime.utcnow(),
        )
        dinner.validate()
        self._dinner_repository.save(dinner)

        event = ConsumptionEvent(
            amount=dinner.amount,
            card_number=dinner.card_number,
            restaurant_code=dinner.restaurant_code,
            timestamp=dinner.timestamp,
        )
        self._event_publisher.publish_consumption(event)
        return dinner
