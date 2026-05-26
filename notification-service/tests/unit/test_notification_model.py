"""Pruebas unitarias para la entidad Notification."""

import pytest
from models.notification import Notification


class TestNotificationModel:
    def test_notification_creation(self):
        notification = Notification(
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

    def test_build_message(self):
        notification = Notification(
            card_number="1234567890",
            restaurant_code="REST-01",
            amount=100.0,
            points=100.0,
            cashback=2.0,
        )
        message = notification.build_message()
        assert "REST-01" in message
        assert "100.00" in message
        assert "2.00" in message
        assert notification.message == message

    def test_build_message_format(self):
        notification = Notification(
            card_number="9876543210",
            restaurant_code="REST-X",
            amount=50.5,
            points=50.5,
            cashback=1.01,
        )
        message = notification.build_message()
        assert "¡Hola!" in message
        assert "Restaurante:" in message
        assert "Consumo:" in message
        assert "Puntos:" in message
        assert "Cashback:" in message
