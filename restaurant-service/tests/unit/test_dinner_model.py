"""Pruebas unitarias para la entidad Dinner."""

import pytest
from models.dinner import Dinner


class TestDinnerValidation:
    def test_valid_dinner_does_not_raise(self):
        dinner = Dinner(amount=50.0, card_number="1234567890", restaurant_code="REST-01")
        dinner.validate()  # no exception

    def test_zero_amount_raises_value_error(self):
        dinner = Dinner(amount=0.0, card_number="1234567890", restaurant_code="REST-01")
        with pytest.raises(ValueError, match="monto"):
            dinner.validate()

    def test_negative_amount_raises_value_error(self):
        dinner = Dinner(amount=-10.0, card_number="1234567890", restaurant_code="REST-01")
        with pytest.raises(ValueError, match="monto"):
            dinner.validate()

    def test_empty_card_number_raises_value_error(self):
        dinner = Dinner(amount=50.0, card_number="", restaurant_code="REST-01")
        with pytest.raises(ValueError, match="tarjeta"):
            dinner.validate()

    def test_empty_restaurant_code_raises_value_error(self):
        dinner = Dinner(amount=50.0, card_number="1234567890", restaurant_code="")
        with pytest.raises(ValueError, match="restaurante"):
            dinner.validate()

    def test_dinner_has_unique_id(self):
        d1 = Dinner(amount=10.0, card_number="A", restaurant_code="R1")
        d2 = Dinner(amount=10.0, card_number="A", restaurant_code="R1")
        assert d1.dinner_id != d2.dinner_id
