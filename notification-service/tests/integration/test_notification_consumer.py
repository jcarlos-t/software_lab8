"""Pruebas de integración para el consumidor de notificaciones."""

from unittest.mock import patch, MagicMock
import pytest

from adapters.rabbitmq.rabbitmq_consumer import RabbitMQConsumer
from adapters.senders.console_sender import ConsoleSender


class TestNotificationConsumer:
    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_consumer_initialization(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="guest",
            password="guest",
        )
        assert consumer._host == "localhost"
        assert consumer._port == 5672
        assert consumer._username == "guest"
        assert consumer._password == "guest"

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_build_service(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        service = consumer._build_service()
        assert service is not None
        assert service._sender is not None
        assert isinstance(service._sender, ConsoleSender)

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_on_message_success(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        
        # Mock channel
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_method.delivery_tag = 1
        
        # Test data
        body = b'{"card_number":"1234567890","restaurant_code":"REST-01","amount":100.0,"points":100.0,"cashback":2.0}'
        
        consumer._on_message(mock_channel, mock_method, None, body)
        
        # Verify message was acknowledged
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=1)

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_on_message_invalid_json(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_method.delivery_tag = 1
        
        # Invalid JSON
        body = b'invalid json'
        
        consumer._on_message(mock_channel, mock_method, None, body)
        
        # Verify message was not acknowledged (nacked)
        mock_channel.basic_nack.assert_called_once_with(delivery_tag=1, requeue=False)
