"""Pruebas unitarias para los métodos start/stop de RabbitMQConsumer."""

from unittest.mock import patch, MagicMock
import pytest

from adapters.rabbitmq.rabbitmq_consumer import RabbitMQConsumer


class TestRabbitMQConsumerStartStop:
    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_stop_when_channel_exists(self, mock_connection):
        consumer = RabbitMQConsumer()
        
        # Mock channel and connection
        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.is_closed = False
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn
        
        # Set up consumer state
        consumer._channel = mock_channel
        consumer._connection = mock_conn
        
        consumer.stop()
        
        # Verify stop_consuming was called
        mock_channel.stop_consuming.assert_called_once()
        
        # Verify connection was closed
        mock_conn.close.assert_called_once()

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_stop_when_no_channel(self, mock_connection):
        consumer = RabbitMQConsumer()
        consumer._channel = None
        consumer._connection = None
        
        # Should not raise an exception
        consumer.stop()

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_stop_when_connection_is_closed(self, mock_connection):
        consumer = RabbitMQConsumer()
        
        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.is_closed = True
        consumer._channel = mock_channel
        consumer._connection = mock_conn
        
        consumer.stop()
        
        # Verify stop_consuming was called
        mock_channel.stop_consuming.assert_called_once()
        
        # Verify close was NOT called since connection is already closed
        mock_conn.close.assert_not_called()

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_start_sets_up_connection_and_channel(self, mock_connection):
        consumer = RabbitMQConsumer()
        
        mock_channel = MagicMock()
        mock_conn = MagicMock()
        mock_conn.channel.return_value = mock_channel
        mock_connection.return_value = mock_conn
        
        # Mock start_consuming to prevent infinite loop
        mock_channel.start_consuming.side_effect = KeyboardInterrupt()
        
        try:
            consumer.start()
        except KeyboardInterrupt:
            pass
        
        # Verify connection was created
        mock_connection.assert_called_once()
        
        # Verify channel was created
        mock_conn.channel.assert_called_once()
        
        # Verify queue was declared
        mock_channel.queue_declare.assert_called_once_with(queue="notification_events", durable=True)
        
        # Verify basic_consume was called
        mock_channel.basic_consume.assert_called_once()
        
        # Verify start_consuming was called
        mock_channel.start_consuming.assert_called_once()
