"""Pruebas unitarias para SendNotificationService."""

from unittest.mock import MagicMock
import pytest

from services.send_notification import SendNotificationService
from models.notification import Notification


class TestSendNotificationService:
    def test_execute_creates_notification(self):
        sender = MagicMock()
        service = SendNotificationService(sender=sender)
        
        notification = service.execute(
            card_number="1234567890",
            restaurant_code="REST-01",
            amount=100.0,
            points=100.0,
            cashback=2.0,
        )
        
        assert notification.card_number == "1234567890"
        assert notification.restaurant_code == "REST-01"
        assert notification.amount == 100.0
        assert notification.points == 100.0
        assert notification.cashback == 2.0

    def test_execute_builds_message(self):
        sender = MagicMock()
        service = SendNotificationService(sender=sender)
        
        notification = service.execute(
            card_number="1234567890",
            restaurant_code="REST-01",
            amount=100.0,
            points=100.0,
            cashback=2.0,
        )
        
        assert notification.message != ""
        assert "REST-01" in notification.message

    def test_execute_calls_sender(self):
        sender = MagicMock()
        service = SendNotificationService(sender=sender)
        
        notification = service.execute(
            card_number="1234567890",
            restaurant_code="REST-01",
            amount=100.0,
            points=100.0,
            cashback=2.0,
        )
        
        sender.send.assert_called_once_with(notification)
