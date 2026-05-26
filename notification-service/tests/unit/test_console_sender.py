"""Pruebas unitarias para ConsoleSender."""

from unittest.mock import patch
import pytest

from adapters.senders.console_sender import ConsoleSender
from models.notification import Notification


class TestConsoleSender:
    @patch("adapters.senders.console_sender.logger")
    @patch("adapters.senders.console_sender.print")
    def test_send_logs_and_prints(self, mock_print, mock_logger):
        sender = ConsoleSender()
        notification = Notification(
            card_number="1234567890",
            restaurant_code="REST-01",
            amount=100.0,
            points=100.0,
            cashback=2.0,
        )
        notification.build_message()
        
        sender.send(notification)
        
        # Verify logger was called
        mock_logger.info.assert_called_once()
        
        # Verify print was called
        mock_print.assert_called_once()
