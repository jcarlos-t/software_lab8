"""Pruebas de integración para el consumidor de recompensas."""

from unittest.mock import patch, MagicMock
import pytest

from adapters.rabbitmq.rabbitmq_consumer import RabbitMQConsumer
from adapters.repositories.in_memory_reward_repo import InMemoryRewardRepository
from models.reward_account import RewardAccount
from shared.events.consumption_event import ConsumptionEvent


class TestRewardsConsumer:
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
        assert service._repo is not None
        assert service._notifier is not None

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
        event = ConsumptionEvent(
            amount=100.0,
            card_number="1234567890",
            restaurant_code="REST-01",
        )
        body = event.to_dict()
        import json
        body_bytes = json.dumps(body).encode()
        
        consumer._on_message(mock_channel, mock_method, None, body_bytes)
        
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

    @patch("adapters.rabbitmq.rabbitmq_consumer.pika.BlockingConnection")
    def test_on_message_creates_account(self, mock_connection):
        consumer = RabbitMQConsumer(
            host="localhost",
            port=5672,
            username="test-user",
            password="test-pass",
        )
        
        # Mock the _build_service to return a service with a shared repo
        shared_repo = InMemoryRewardRepository()
        mock_service = MagicMock()
        mock_service._repo = shared_repo
        mock_service.execute = MagicMock(side_effect=lambda event: shared_repo.save(
            RewardAccount(card_number=event.card_number)
        ))
        
        consumer._build_service = MagicMock(return_value=mock_service)
        
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_method.delivery_tag = 1
        
        event = ConsumptionEvent(
            amount=100.0,
            card_number="NEW_CARD",
            restaurant_code="REST-01",
        )
        body = event.to_dict()
        import json
        body_bytes = json.dumps(body).encode()
        
        consumer._on_message(mock_channel, mock_method, None, body_bytes)
        
        # Verify account was created and stored
        account = shared_repo.find_by_card("NEW_CARD")
        assert account is not None
