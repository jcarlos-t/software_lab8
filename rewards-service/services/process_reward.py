from models.reward_account import RewardAccount
from ports.reward_repository import RewardRepository
from ports.notification_publisher import NotificationPublisher
from services.calculate_points import CalculatePointsService
from services.calculate_cashback import CalculateCashbackService
from shared.events.consumption_event import ConsumptionEvent


class ProcessRewardService:
    """Caso de uso orquestador: procesa un evento de consumo y actualiza la cuenta."""

    def __init__(
        self,
        reward_repository: RewardRepository,
        notification_publisher: NotificationPublisher,
    ) -> None:
        self._repo = reward_repository
        self._notifier = notification_publisher
        self._points_svc = CalculatePointsService()
        self._cashback_svc = CalculateCashbackService()

    def execute(self, event: ConsumptionEvent) -> RewardAccount:
        """
        Procesa el evento: calcula puntos y cashback, actualiza el saldo
        y publica un evento de notificación.

        Returns:
            Cuenta de recompensas actualizada.
        """
        points = self._points_svc.execute(event.amount, event.restaurant_code)
        cashback = self._cashback_svc.execute(event.amount, event.restaurant_code)

        account = self._repo.find_by_card(event.card_number) or RewardAccount(
            card_number=event.card_number
        )
        account.add_points(points)
        account.add_cashback(cashback)
        self._repo.save(account)

        self._notifier.publish_reward_processed(event, points, cashback)
        return account
