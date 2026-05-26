from models.notification import Notification
from ports.notification_sender import NotificationSender


class SendNotificationService:
    """Caso de uso: Enviar notificación de recompensa al cliente."""

    def __init__(self, sender: NotificationSender) -> None:
        self._sender = sender

    def execute(
        self,
        card_number: str,
        restaurant_code: str,
        amount: float,
        points: float,
        cashback: float,
    ) -> Notification:
        notification = Notification(
            card_number=card_number,
            restaurant_code=restaurant_code,
            amount=amount,
            points=points,
            cashback=cashback,
        )
        notification.build_message()
        self._sender.send(notification)
        return notification
