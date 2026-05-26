"""CLI alternativo para registrar cenas desde la línea de comandos."""

import argparse
import sys
from datetime import datetime

from services.register_dinner import (
    RegisterDinnerCommand,
    RegisterDinnerService,
)
from adapters.repositories.in_memory_dinner_repo import InMemoryDinnerRepository
from adapters.repositories.rabbitmq_publisher import RabbitMQEventPublisher


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Registrar una cena desde CLI")
    parser.add_argument("--amount", type=float, required=True, help="Monto total")
    parser.add_argument("--card", required=True, help="Número de tarjeta del cliente")
    parser.add_argument("--restaurant", required=True, help="Código del restaurante")
    args = parser.parse_args(argv)

    service = RegisterDinnerService(
        dinner_repository=InMemoryDinnerRepository(),
        event_publisher=RabbitMQEventPublisher(),
    )
    command = RegisterDinnerCommand(
        amount=args.amount,
        card_number=args.card,
        restaurant_code=args.restaurant,
        timestamp=datetime.utcnow(),
    )
    try:
        dinner = service.execute(command)
        print(f"[OK] Cena registrada: {dinner.dinner_id}")
        return 0
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
