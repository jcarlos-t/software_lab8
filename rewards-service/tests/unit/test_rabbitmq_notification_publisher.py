"""Pruebas unitarias para RabbitMQNotificationPublisher."""

from unittest.mock import patch, MagicMock

from adapters.rabbitmq.rabbitmq_notification_publisher import RabbitMQNotificationPublisher
from shared.events.consumption_event import ConsumptionEvent


class TestRabbitMQNotificationPublisher:
    @patch("adapters.rabbitmq.rabbitmq_notification_publisher.pika.BlockingConnection")
    def test_publish_reward_processed(self, mock_connection):
        mock_conn = MagicMock()
        mock_channel = MagicMock()
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn

        publisher = RabbitMQNotificationPublisher(
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

        publisher.publish_reward_processed(event, 100.0, 2.0)

        mock_channel.queue_declare.assert_called_once_with(queue="notification_events", durable=True)
        mock_channel.basic_publish.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("adapters.rabbitmq.rabbitmq_notification_publisher.pika.BlockingConnection")
    def test_publish_reward_processed_uses_correct_credentials(self, mock_connection):
        publisher = RabbitMQNotificationPublisher(
            host="test-host",
            port=5673,
            username="test-user",
            password="test-pass",
        )

        event = ConsumptionEvent(amount=50.0, card_number="123", restaurant_code="R1")
        publisher.publish_reward_processed(event, 50.0, 1.0)

        mock_connection.assert_called_once()
        call_args = mock_connection.call_args
        assert call_args is not None

    @patch("adapters.rabbitmq.rabbitmq_notification_publisher.pika.BlockingConnection")
    def test_publish_reward_processed_creates_correct_message_body(self, mock_connection):
        mock_conn = MagicMock()
        mock_channel = MagicMock()
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn

        publisher = RabbitMQNotificationPublisher(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        event = ConsumptionEvent(
            amount=150.0,
            card_number="99998888",
            restaurant_code="TEST-01",
        )

        publisher.publish_reward_processed(event, 150.0, 3.0)

        call_args = mock_channel.basic_publish.call_args
        assert call_args is not None
        kwargs = call_args.kwargs or {}
        body = kwargs.get("body")
        assert body is not None
        assert "99998888" in body
        assert "TEST-01" in body
        assert "150.0" in body
        assert "3.0" in body
