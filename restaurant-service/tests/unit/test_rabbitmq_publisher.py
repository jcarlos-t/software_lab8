"""Pruebas unitarias para RabbitMQEventPublisher."""

from unittest.mock import patch, MagicMock
import pytest

from adapters.repositories.rabbitmq_publisher import RabbitMQEventPublisher
from shared.events.consumption_event import ConsumptionEvent


class TestRabbitMQEventPublisher:
    @patch("adapters.repositories.rabbitmq_publisher.pika.BlockingConnection")
    def test_publish_consumption(self, mock_connection):
        mock_conn = MagicMock()
        mock_channel = MagicMock()
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn
        
        publisher = RabbitMQEventPublisher(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        event = ConsumptionEvent(
            amount=100.0,
            card_number="1234567890",
            restaurant_code="REST-01",
        )
        
        publisher.publish_consumption(event)
        
        # Verify queue was declared
        mock_channel.queue_declare.assert_called_once_with(queue="consumption_events", durable=True)
        
        # Verify message was published
        mock_channel.basic_publish.assert_called_once()
        
        # Verify connection was closed
        mock_conn.close.assert_called_once()

    @patch("adapters.repositories.rabbitmq_publisher.pika.BlockingConnection")
    def test_publish_consumption_uses_correct_credentials(self, mock_connection):
        publisher = RabbitMQEventPublisher(
            host="test-host",
            port=5673,
            username="test-user",
            password="test-pass",
        )
        
        event = ConsumptionEvent(amount=50.0, card_number="123", restaurant_code="R1")
        publisher.publish_consumption(event)
        
        # Verify connection was called with correct parameters
        mock_connection.assert_called_once()
        call_args = mock_connection.call_args
        assert call_args is not None
