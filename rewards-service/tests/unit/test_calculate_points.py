"""Pruebas unitarias para los servicios de cálculo de puntos y cashback."""

import pytest
from services.calculate_points import CalculatePointsService
from services.calculate_cashback import CalculateCashbackService


class TestCalculatePointsService:
    def test_points_calculated_correctly(self):
        svc = CalculatePointsService()
        result = svc.execute(amount=100.0, restaurant_code="REST-01")
        assert result == 100.0  # 1 punto por sol gastado (default)

    def test_zero_amount_returns_zero(self):
        svc = CalculatePointsService()
        assert svc.execute(0.0, "REST-01") == 0.0

    def test_fractional_amount(self):
        svc = CalculatePointsService()
        result = svc.execute(amount=33.33, restaurant_code="REST-X")
        assert result == 33.33


class TestCalculateCashbackService:
    def test_cashback_calculated_correctly(self):
        svc = CalculateCashbackService()
        result = svc.execute(amount=100.0, restaurant_code="REST-01")
        assert result == 2.0  # 2% de 100

    def test_zero_amount_returns_zero(self):
        svc = CalculateCashbackService()
        assert svc.execute(0.0, "REST-01") == 0.0

    def test_cashback_precision(self):
        svc = CalculateCashbackService()
        result = svc.execute(amount=150.0, restaurant_code="REST-01")
        assert result == 3.0
