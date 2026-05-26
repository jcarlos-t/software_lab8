"""Pruebas unitarias para RewardRule."""

import pytest
from models.reward_rule import RewardRule


class TestRewardRule:
    def test_calculate_points_default(self):
        rule = RewardRule(restaurant_code="REST-01")
        points = rule.calculate_points(100.0)
        assert points == 100.0  # 1 punto por sol

    def test_calculate_points_custom_rate(self):
        rule = RewardRule(restaurant_code="REST-01", points_per_unit=2.0)
        points = rule.calculate_points(100.0)
        assert points == 200.0  # 2 puntos por sol

    def test_calculate_cashback_default(self):
        rule = RewardRule(restaurant_code="REST-01")
        cashback = rule.calculate_cashback(100.0)
        assert cashback == 2.0  # 2% de 100

    def test_calculate_cashback_custom_rate(self):
        rule = RewardRule(restaurant_code="REST-01", cashback_rate=0.05)
        cashback = rule.calculate_cashback(100.0)
        assert cashback == 5.0  # 5% de 100

    def test_rule_is_frozen(self):
        from dataclasses import FrozenInstanceError
        rule = RewardRule(restaurant_code="REST-01")
        with pytest.raises(FrozenInstanceError):
            rule.restaurant_code = "REST-02"
