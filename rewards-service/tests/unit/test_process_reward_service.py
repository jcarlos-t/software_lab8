"""Pruebas unitarias para ProcessRewardService."""

from datetime import datetime
from unittest.mock import MagicMock
import pytest

from services.process_reward import ProcessRewardService
from adapters.repositories.in_memory_reward_repo import InMemoryRewardRepository
from shared.events.consumption_event import ConsumptionEvent


class TestProcessRewardService:
    def _make_event(self, amount: float = 100.0, card: str = "4444") -> ConsumptionEvent:
        return ConsumptionEvent(
            amount=amount,
            card_number=card,
            restaurant_code="RESTP",
            timestamp=datetime.utcnow(),
        )

    def _make_service(self, notifier=None):
        repo = InMemoryRewardRepository()
        notif = notifier or MagicMock()
        return ProcessRewardService(reward_repository=repo, notification_publisher=notif), repo, notif

    def test_creates_account_if_not_exists(self):
        svc, repo, _ = self._make_service()
        event = self._make_event(card="NEW_CARD")
        svc.execute(event)
        acc = repo.find_by_card("NEW_CARD")
        assert acc is not None

    def test_points_and_cashback_added(self):
        svc, repo, _ = self._make_service()
        event = self._make_event(amount=200.0, card="1234")
        account = svc.execute(event)
        assert account.points_balance == 200.0
        assert account.cashback_balance == 4.0  # 2% de 200

    def test_accumulates_on_existing_account(self):
        svc, repo, _ = self._make_service()
        event1 = self._make_event(amount=100.0, card="5555")
        event2 = self._make_event(amount=50.0, card="5555")
        svc.execute(event1)
        svc.execute(event2)
        acc = repo.find_by_card("5555")
        assert acc.points_balance == 150.0
        assert round(acc.cashback_balance, 2) == 3.0

    def test_notifier_is_called(self):
        svc, _, notif = self._make_service()
        event = self._make_event()
        svc.execute(event)
        notif.publish_reward_processed.assert_called_once()
