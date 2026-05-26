"""Pruebas unitarias para la entidad Client."""

import pytest
from models.client import Client


class TestClientModel:
    def test_client_creation(self):
        client = Client(
            card_number="1234567890",
            name="Juan Perez",
            email="juan@example.com",
        )
        assert client.card_number == "1234567890"
        assert client.name == "Juan Perez"
        assert client.email == "juan@example.com"

    def test_is_new_with_name(self):
        client = Client(card_number="1234567890", name="Juan Perez")
        assert not client.is_new()

    def test_is_new_without_name(self):
        client = Client(card_number="1234567890")
        assert client.is_new()

    def test_is_new_with_empty_name(self):
        client = Client(card_number="1234567890", name="")
        assert client.is_new()
