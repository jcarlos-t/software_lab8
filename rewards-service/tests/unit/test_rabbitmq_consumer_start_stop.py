"""Pruebas unitarias para los métodos start/stop de RabbitMQConsumer del rewards-service."""

from unittest.mock import patch, MagicMock

from adapters.rabbitmq.rabbitmq_consumer import RabbitMQConsumer


class TestRabbitMQConsumerStartStop:
    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_stop_when_channel_exists(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )

        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.is_closed = False
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn

        consumer._channel = mock_channel
        consumer._connection = mock_conn

        consumer.stop()

        mock_channel.stop_consuming.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_stop_when_no_channel(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        consumer._channel = None
        consumer._connection = None

        consumer.stop()

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_stop_when_connection_is_closed(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )

        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.is_closed = True
        consumer._channel = mock_channel
        consumer._connection = mock_conn

        consumer.stop()

        mock_channel.stop_consuming.assert_called_once()
        mock_conn.close.assert_not_called()

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_start_sets_up_connection_and_channel(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )

        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn

        mock_channel.start_consuming.side_effect = KeyboardInterrupt()

        try:
            consumer.start()
        except KeyboardInterrupt:
            pass

        mock_connection.assert_called_once()
        mock_conn.channel.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue="consumption_events", durable=True)
        mock_channel.basic_qos.assert_called_once_with(prefetch_count=1)
        mock_channel.basic_consume.assert_called_once()
        mock_channel.start_consuming.assert_called_once()
