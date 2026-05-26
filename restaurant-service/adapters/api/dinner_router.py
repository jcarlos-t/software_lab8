import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime

from services.register_dinner import (
    RegisterDinnerCommand,
    RegisterDinnerService,
)
from adapters.repositories.in_memory_dinner_repo import InMemoryDinnerRepository
from adapters.rabbitmq.rabbitmq_publisher import RabbitMQEventPublisher

router = APIRouter(prefix="/dinners", tags=["dinners"])

def _build_service() -> RegisterDinnerService:
    return RegisterDinnerService(
        dinner_repository=InMemoryDinnerRepository(),
        event_publisher=RabbitMQEventPublisher(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT")),
            username=os.getenv("RABBITMQ_USER"),
            password=os.getenv("RABBITMQ_PASS"),
            virtual_host=os.getenv("RABBITMQ_VHOST"),
        ),
    )


class DinnerRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Monto total de la cena")
    card_number: str = Field(..., min_length=4)
    restaurant_code: str = Field(..., min_length=1)
    timestamp: datetime | None = None


class DinnerResponse(BaseModel):
    dinner_id: str
    amount: float
    card_number: str
    restaurant_code: str
    timestamp: datetime


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva cena",
)
def register_dinner(body: DinnerRequest) -> DinnerResponse:
    """
    Registra la cena del cliente y publica el evento de consumo al broker.
    """
    service = _build_service()
    try:
        command = RegisterDinnerCommand(
            amount=body.amount,
            card_number=body.card_number,
            restaurant_code=body.restaurant_code,
            timestamp=body.timestamp,
        )
        dinner = service.execute(command)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return DinnerResponse(
        dinner_id=dinner.dinner_id,
        amount=dinner.amount,
        card_number=dinner.card_number,
        restaurant_code=dinner.restaurant_code,
        timestamp=dinner.timestamp,
    )
