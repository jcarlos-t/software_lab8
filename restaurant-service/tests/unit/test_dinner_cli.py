"""Pruebas unitarias para el CLI de registro de cenas."""

from unittest.mock import patch, MagicMock
import pytest

from adapters.dinner_cli import main


class TestDinnerCLI:
    @patch("adapters.dinner_cli.RegisterDinnerService")
    @patch("adapters.dinner_cli.RabbitMQEventPublisher")
    @patch("adapters.dinner_cli.InMemoryDinnerRepository")
    def test_main_success(self, mock_repo, mock_publisher, mock_service):
        mock_dinner = MagicMock()
        mock_dinner.dinner_id = "test-id-123"
        mock_service_instance = MagicMock()
        mock_service_instance.execute.return_value = mock_dinner
        mock_service.return_value = mock_service_instance
        
        result = main(["--amount", "100.0", "--card", "1234567890", "--restaurant", "REST-01"])
        
        assert result == 0
        mock_service_instance.execute.assert_called_once()

    @patch("adapters.dinner_cli.RegisterDinnerService")
    @patch("adapters.dinner_cli.RabbitMQEventPublisher")
    @patch("adapters.dinner_cli.InMemoryDinnerRepository")
    def test_main_invalid_amount(self, mock_repo, mock_publisher, mock_service):
        mock_service_instance = MagicMock()
        mock_service_instance.execute.side_effect = ValueError("El monto debe ser mayor a cero")
        mock_service.return_value = mock_service_instance
        
        result = main(["--amount", "0.0", "--card", "1234567890", "--restaurant", "REST-01"])
        
        assert result == 1

    @patch("adapters.dinner_cli.RegisterDinnerService")
    @patch("adapters.dinner_cli.RabbitMQEventPublisher")
    @patch("adapters.dinner_cli.InMemoryDinnerRepository")
    def test_main_missing_required_args(self, mock_repo, mock_publisher, mock_service):
        # Missing --amount
        with pytest.raises(SystemExit):
            main(["--card", "1234567890", "--restaurant", "REST-01"])
