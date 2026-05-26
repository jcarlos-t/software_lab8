"""Pruebas unitarias para el manejo de errores en dinner_router."""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from main import app


class TestDinnerRouterErrorHandling:
    def test_post_dinner_empty_card_number(self):
        client = TestClient(app)
        payload = {
            "amount": 100.0,
            "card_number": "",
            "restaurant_code": "REST-01",
        }
        response = client.post("/dinners/", json=payload)
        assert response.status_code == 422

    def test_post_dinner_empty_restaurant_code(self):
        client = TestClient(app)
        payload = {
            "amount": 100.0,
            "card_number": "1234567890",
            "restaurant_code": "",
        }
        response = client.post("/dinners/", json=payload)
        assert response.status_code == 422
