import logging

from models.notification import Notification
from ports.notification_sender import NotificationSender

logger = logging.getLogger(__name__)


class ConsoleSender(NotificationSender):
    """Adaptador de salida mock: imprime la notificación en la consola/log."""

    def send(self, notification: Notification) -> None:
        logger.info("[NOTIFICACIÓN] Tarjeta: %s\n%s", notification.card_number, notification.message)
        print(f"[NOTIFICACIÓN] {notification.message}")
