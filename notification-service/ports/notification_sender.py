from abc import ABC, abstractmethod
from models.notification import Notification


class NotificationSender(ABC):
    """Puerto de salida: envía la notificación al cliente."""

    @abstractmethod
    def send(self, notification: Notification) -> None:
        ...
