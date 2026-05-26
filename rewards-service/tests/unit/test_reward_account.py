"""Pruebas unitarias para RewardAccount."""

import pytest
from models.reward_account import RewardAccount


class TestRewardAccount:
    def test_account_creation(self):
        account = RewardAccount(card_number="1234567890")
        assert account.card_number == "1234567890"
        assert account.points_balance == 0.0
        assert account.cashback_balance == 0.0

    def test_add_points(self):
        account = RewardAccount(card_number="1234567890")
        account.add_points(100.0)
        assert account.points_balance == 100.0

    def test_add_points_negative_raises(self):
        account = RewardAccount(card_number="1234567890")
        with pytest.raises(ValueError, match="negativos"):
            account.add_points(-10.0)

    def test_add_cashback(self):
        account = RewardAccount(card_number="1234567890")
        account.add_cashback(5.0)
        assert account.cashback_balance == 5.0

    def test_add_cashback_negative_raises(self):
        account = RewardAccount(card_number="1234567890")
        with pytest.raises(ValueError, match="negativo"):
            account.add_cashback(-5.0)

    def test_total_value(self):
        account = RewardAccount(card_number="1234567890")
        account.add_points(100.0)
        account.add_cashback(5.0)
        assert account.total_value() == 105.0
