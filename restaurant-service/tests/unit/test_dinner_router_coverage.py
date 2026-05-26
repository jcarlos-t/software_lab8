"""Pruebas adicionales para mejorar cobertura de dinner_router."""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from main import app


class TestDinnerRouterCoverage:
    def test_post_dinner_zero_amount_validation(self):
        """Test para cubrir validación de monto cero en el router."""
        client = TestClient(app)
        payload = {
            "amount": 0.0,
            "card_number": "1234567890",
            "restaurant_code": "REST-01",
        }
        response = client.post("/dinners/", json=payload)
        assert response.status_code == 422

    def test_post_dinner_negative_amount_validation(self):
        """Test para cubrir validación de monto negativo en el router."""
        client = TestClient(app)
        payload = {
            "amount": -10.0,
            "card_number": "1234567890",
            "restaurant_code": "REST-01",
        }
        response = client.post("/dinners/", json=payload)
        assert response.status_code == 422
