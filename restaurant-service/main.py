"""Entry point del Restaurant Service."""

import os
import uvicorn
from fastapi import FastAPI
from adapters.api.dinner_router import router

app = FastAPI(
    title="Restaurant Service",
    description="Registra cenas y publica eventos de consumo al broker.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "service": "restaurant-service"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8001")),
        reload=True,
    )
