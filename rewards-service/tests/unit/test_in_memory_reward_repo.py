"""Pruebas unitarias para InMemoryRewardRepository."""

from models.reward_account import RewardAccount
from adapters.repositories.in_memory_reward_repo import InMemoryRewardRepository


class TestInMemoryRewardRepository:
    def test_save_and_find_by_card(self):
        repo = InMemoryRewardRepository()
        account = RewardAccount(card_number="1234567890")
        account.add_points(100.0)
        
        repo.save(account)
        found = repo.find_by_card("1234567890")
        
        assert found is not None
        assert found.card_number == "1234567890"
        assert found.points_balance == 100.0

    def test_find_by_card_not_found(self):
        repo = InMemoryRewardRepository()
        found = repo.find_by_card("non-existent-card")
        assert found is None

    def test_count_property(self):
        repo = InMemoryRewardRepository()
        assert repo.count == 0
        
        repo.save(RewardAccount(card_number="123"))
        assert repo.count == 1
        
        repo.save(RewardAccount(card_number="456"))
        assert repo.count == 2
