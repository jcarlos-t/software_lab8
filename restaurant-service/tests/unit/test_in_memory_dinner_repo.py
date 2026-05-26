"""Pruebas unitarias para InMemoryDinnerRepository."""

from models.dinner import Dinner
from adapters.repositories.in_memory_dinner_repo import InMemoryDinnerRepository


class TestInMemoryDinnerRepository:
    def test_save_and_find_by_id(self):
        repo = InMemoryDinnerRepository()
        dinner = Dinner(amount=100.0, card_number="1234567890", restaurant_code="REST-01")
        
        repo.save(dinner)
        found = repo.find_by_id(dinner.dinner_id)
        
        assert found is not None
        assert found.dinner_id == dinner.dinner_id
        assert found.amount == 100.0

    def test_find_by_id_not_found(self):
        repo = InMemoryDinnerRepository()
        found = repo.find_by_id("non-existent-id")
        assert found is None

    def test_count_property(self):
        repo = InMemoryDinnerRepository()
        assert repo.count == 0
        
        repo.save(Dinner(amount=100.0, card_number="123", restaurant_code="R1"))
        assert repo.count == 1
        
        repo.save(Dinner(amount=200.0, card_number="456", restaurant_code="R2"))
        assert repo.count == 2
