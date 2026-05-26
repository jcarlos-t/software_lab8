"""Pruebas unitarias para el servicio RegisterDinnerService."""

from unittest.mock import MagicMock, call
import pytest

from models.dinner import Dinner
from services.register_dinner import (
    RegisterDinnerCommand,
    RegisterDinnerService,
)
from adapters.repositories.in_memory_dinner_repo import InMemoryDinnerRepository
from shared.events.consumption_event import ConsumptionEvent


class TestRegisterDinnerService:
    def _make_service(self, publisher=None):
        repo = InMemoryDinnerRepository()
        pub = publisher or MagicMock()
        return RegisterDinnerService(dinner_repository=repo, event_publisher=pub), repo, pub

    def test_execute_saves_dinner(self):
        service, repo, _ = self._make_service()
        cmd = RegisterDinnerCommand(amount=100.0, card_number="4444", restaurant_code="R01")
        dinner = service.execute(cmd)
        assert repo.find_by_id(dinner.dinner_id) is not None

    def test_execute_publishes_event(self):
        service, _, publisher = self._make_service()
        cmd = RegisterDinnerCommand(amount=75.5, card_number="9999", restaurant_code="R02")
        service.execute(cmd)
        publisher.publish_consumption.assert_called_once()
        event: ConsumptionEvent = publisher.publish_consumption.call_args[0][0]
        assert event.amount == 75.5
        assert event.card_number == "9999"
        assert event.restaurant_code == "R02"

    def test_execute_raises_on_invalid_amount(self):
        service, _, _ = self._make_service()
        cmd = RegisterDinnerCommand(amount=0.0, card_number="1234", restaurant_code="R01")
        with pytest.raises(ValueError):
            service.execute(cmd)

    def test_execute_raises_on_empty_card(self):
        service, _, _ = self._make_service()
        cmd = RegisterDinnerCommand(amount=10.0, card_number="", restaurant_code="R01")
        with pytest.raises(ValueError):
            service.execute(cmd)

    def test_execute_returns_dinner_with_correct_data(self):
        service, _, _ = self._make_service()
        cmd = RegisterDinnerCommand(amount=200.0, card_number="5555", restaurant_code="RTEST")
        dinner = service.execute(cmd)
        assert dinner.amount == 200.0
        assert dinner.card_number == "5555"
        assert dinner.restaurant_code == "RTEST"
