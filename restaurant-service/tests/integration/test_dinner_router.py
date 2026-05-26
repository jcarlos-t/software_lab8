"""Pruebas de integración para el router REST del restaurant-service."""

from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestDinnerRouter:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @patch("adapters.repositories.rabbitmq_publisher.RabbitMQEventPublisher.publish_consumption")
    def test_post_dinner_success(self, mock_pub):
        mock_pub.return_value = None
        payload = {
            "amount": 120.0,
            "card_number": "1234567890",
            "restaurant_code": "REST-01",
        }
        response = client.post("/dinners/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 120.0
        assert data["card_number"] == "1234567890"
        assert "dinner_id" in data

    @patch("adapters.repositories.rabbitmq_publisher.RabbitMQEventPublisher.publish_consumption")
    def test_post_dinner_invalid_amount(self, mock_pub):
        payload = {
            "amount": -5.0,
            "card_number": "1234567890",
            "restaurant_code": "REST-01",
        }
        response = client.post("/dinners/", json=payload)
        assert response.status_code == 422
