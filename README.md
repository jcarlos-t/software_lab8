# Sistema de Recompensas - Laboratorio 8

Sistema de recompensas para restaurantes implementado con arquitectura orientada a eventos y hexagonal (Ports & Adapters) en Python.

## Arquitectura

### Nivel Macro: Arquitectura Orientada a Eventos (EDA)

El sistema utiliza RabbitMQ como broker de mensajería para desacoplar tres microservicios:

**Colas del sistema:**
- `consumption_events` — el Restaurant Service publica eventos de cena; el Rewards Service los consume
- `notification_events` — el Rewards Service publica eventos de recompensa procesada; el Notification Service los consume

**Servicios:**

```
                    ┌──────────────────┐
                    │    RabbitMQ      │
                    │     Broker       │
                    └──┬───────────┬───┘
                       │           │
          publish      │           │      consume
    ┌──────────────────┘           └──────────────────┐
    ▼                                                    ▼
┌─────────────────┐                        ┌──────────────────────┐
│ Restaurant Svc  │                        │    Rewards Svc       │
│ (API / CLI)     │─── consumption_events ──→│ (Consumer)          │
│ Registra cenas  │                        │ Calcula puntos/      │
│ y publica       │                        │ cashback, actualiza  │
│ eventos         │                        │ cuenta, publica      │
└─────────────────┘                        │ notificación         │
                                           └──────────┬───────────┘
                                                      │
                                                      │ notification_events
                                                      │
                                                      ▼
                                           ┌──────────────────────┐
                                           │ Notification Svc     │
                                           │ (Consumer)           │
                                           │ Envía notificación   │
                                           │ al cliente (consola) │
                                           └──────────────────────┘
```

### Nivel Micro: Arquitectura Hexagonal (Ports & Adapters)

Cada servicio separa la lógica de negocio (dominio) de los detalles técnicos mediante puertos (interfaces abstractas) y adaptadores (implementaciones concretas).

| Capa          | Contenido                                                   |
|---------------|-------------------------------------------------------------|
| **models/**   | Entidades/value objects del dominio (Dinner, RewardAccount, Notification, RewardRule) |
| **services/** | Casos de uso — orquestan la lógica de negocio pura          |
| **ports/**    | Contratos/interfaces abstractas para comunicación externa    |
| **adapters/** | Implementaciones concretas de los puertos (RabbitMQ, APIs, repos en memoria, CLI) |

**Inbound adapters** (cómo llegan los datos al dominio):
- API REST (`adapters/api/`) — Restaurant Service
- CLI (`adapters/dinner_cli.py`) — Restaurant Service
- RabbitMQ consumers (`adapters/rabbitmq/`) — Rewards & Notification Services

**Outbound adapters** (cómo el dominio se comunica con el exterior):
- RabbitMQ publishers (`adapters/repositories/`) — publicación de eventos
- Repositorios en memoria (`adapters/repositories/`) — persistencia temporal
- Console sender (`adapters/senders/`) — envío de notificaciones por consola

## Estructura del Proyecto

```
software_lab8/
├── restaurant-service/                # API REST + CLI para registro de cenas
│   ├── models/
│   │   ├── dinner.py                  # Entidad Dinner
│   │   └── client.py                  # Value Object Client
│   ├── services/
│   │   └── register_dinner.py         # Caso de uso: registrar cena
│   ├── ports/
│   │   ├── event_publisher.py         # Puerto de salida para eventos
│   │   └── dinner_repository.py       # Puerto de salida para persistencia
│   ├── adapters/
│   │   ├── api/dinner_router.py       # Adaptador de entrada: API REST
│   │   ├── dinner_cli.py              # Adaptador de entrada: CLI
│   │   └── repositories/
│   │       ├── rabbitmq_publisher.py  # Adaptador de salida: RabbitMQ
│   │       └── in_memory_dinner_repo.py # Adaptador de salida: repositorio en memoria
│   ├── tests/
│   │   ├── unit/                      # Pruebas unitarias
│   │   └── integration/               # Pruebas de integración
│   ├── shared/                        # Copia local del módulo compartido
│   ├── main.py                        # Entry point FastAPI
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── rewards-service/                   # Consumidor de eventos, calcula recompensas
│   ├── models/
│   │   ├── reward_account.py          # Entidad cuenta de recompensas
│   │   └── reward_rule.py             # Value Object regla de cálculo
│   ├── services/
│   │   ├── process_reward.py          # Caso de uso orquestador
│   │   ├── calculate_points.py        # Servicio de cálculo de puntos
│   │   └── calculate_cashback.py      # Servicio de cálculo de cashback
│   ├── ports/
│   │   ├── reward_repository.py       # Puerto de salida para persistencia
│   │   └── notification_publisher.py  # Puerto de salida para notificaciones
│   ├── adapters/
│   │   ├── rabbitmq/
│   │   │   └── rabbitmq_consumer.py   # Adaptador de entrada: RabbitMQ consumer
│   │   └── repositories/
│   │       ├── in_memory_reward_repo.py      # Repositorio en memoria
│   │       └── rabbitmq_notification_publisher.py # Adaptador de salida: RabbitMQ
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── shared/                        # Copia local del módulo compartido
│   ├── main.py                        # Entry point del consumer
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── notification-service/              # Consumidor de eventos, envía notificaciones
│   ├── models/
│   │   └── notification.py            # Entidad Notification
│   ├── services/
│   │   └── send_notification.py       # Caso de uso: enviar notificación
│   ├── ports/
│   │   └── notification_sender.py     # Puerto de salida para envío
│   ├── adapters/
│   │   ├── rabbitmq/
│   │   │   └── rabbitmq_consumer.py   # Adaptador de entrada: RabbitMQ consumer
│   │   └── senders/
│   │       └── console_sender.py      # Adaptador de salida: notificación por consola
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── shared/                        # Copia local del módulo compartido
│   ├── main.py                        # Entry point del consumer
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── shared/                            # Módulo compartido (instalable vía pyproject.toml)
│   └── src/shared/
│       ├── events/
│       │   └── consumption_event.py   # Evento de dominio: ConsumptionEvent
│       └── messaging/
│           ├── consumer.py            # Puerto abstracto AbstractConsumer
│           └── publisher.py           # Puerto abstracto AbstractPublisher
├── docker/                            # Recursos Docker
├── docker-compose.yml                 # Orquestación de servicios
├── sonar-project.properties           # Configuración SonarCloud
└── .gitignore
```

## Flujo del Sistema

```
1. POST /dinners/  ──→  Restaurant Service  ──→  RabbitMQ (consumption_events)
                                                         │
                                                         ▼
2.                                               Rewards Service
                                                  ├── Calcula puntos y cashback
                                                  ├── Actualiza RewardAccount
                                                  └── Publica en RabbitMQ (notification_events)
                                                         │
                                                         ▼
3.                                               Notification Service
                                                  └── Envía notificación al cliente (consola)
```

### Evento de Consumo (formato JSON)

```json
{
  "event_id": "uuid",
  "amount": 150.0,
  "card_number": "1234567890",
  "restaurant_code": "REST-01",
  "timestamp": "2025-05-25T12:00:00"
}
```

## Requisitos Técnicos

| Requisito      | Versión    |
|----------------|------------|
| **Python**     | ≥ 3.11     |
| **RabbitMQ**   | 3.12+      |
| **FastAPI**    | ≥ 0.110    |
| **Pika**       | ≥ 1.3.2    |
| **Pytest**     | ≥ 8.1      |
| **Docker**     | cualquier  |

## Ejecución

### Con Docker Compose (Recomendado)

```bash
docker compose up -d
```

Esto inicia:
- RabbitMQ (gestión en http://localhost:15672)
- Restaurant Service (http://localhost:8001)
- Rewards Service
- Notification Service

### Localmente

1. Iniciar RabbitMQ:
```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

2. Instalar dependencias:
```bash
cd shared && pip install -e . && cd ..
for svc in restaurant-service rewards-service notification-service; do
  cd $svc && pip install -r requirements.txt && cd ..
done
```

3. Ejecutar servicios (tres terminales):
```bash
# Terminal 1 - Restaurant Service (API: http://localhost:8001)
cd restaurant-service && python main.py

# Terminal 2 - Rewards Service
cd rewards-service && python main.py

# Terminal 3 - Notification Service
cd notification-service && python main.py
```

### Alternativa: CLI del Restaurant Service

```bash
cd restaurant-service && python -m adapters.dinner_cli --amount 100 --card 1234567890 --restaurant REST-01
```

## Pruebas

Ejecutar pruebas por servicio:

```bash
cd restaurant-service && pytest --cov=. --cov-report=xml --cov-report=html
cd rewards-service    && pytest --cov=. --cov-report=xml --cov-report=html
cd notification-service && pytest --cov=. --cov-report=xml --cov-report=html
```

O desde la raíz con el script auxiliar (si existe):
```bash
# Ejecutar todas las pruebas y generar coverage combinado
for svc in restaurant-service rewards-service notification-service; do
  (cd $svc && pytest --cov=. --cov-report=xml --cov-report=html)
done
```

## Calidad de Código

El proyecto se analiza vía **SonarCloud** (o SonarQube si se usa el servidor del curso):

| Atributo           | Objetivo             |
|--------------------|----------------------|
| Reliability        | A (Sin bugs)         |
| Security           | A (Sin vulnerabilidades) |
| Maintainability    | A (Deuda técnica < 5%) |
| Duplications       | < 3%                 |
| Test Coverage      | ≥ 85%                |

## API Endpoints (Restaurant Service)

| Método | Ruta          | Descripción                       |
|--------|---------------|-----------------------------------|
| POST   | `/dinners/`   | Registrar una nueva cena          |
| GET    | `/health`     | Health check del servicio         |

### Ejemplo: `POST /dinners/`

```bash
curl -X POST http://localhost:8001/dinners/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.0, "card_number": "1234567890", "restaurant_code": "REST-01"}'
```

Respuesta:
```json
{
  "dinner_id": "uuid",
  "amount": 100.0,
  "card_number": "1234567890",
  "restaurant_code": "REST-01",
  "timestamp": "2025-05-25T12:00:00"
}
```

## Principios de Diseño Aplicados

| Principio        | Cómo se aplica                                        |
|------------------|-------------------------------------------------------|
| **Alta cohesión**  | Cada servicio y cada módulo tiene una responsabilidad única y bien definida |
| **Bajo acoplamiento** | Los servicios se comunican exclusivamente mediante eventos asíncronos vía RabbitMQ |
| **Modularidad**     | Separación clara en capas (models, services, ports, adapters) dentro de cada servicio |
| **Abstracción**     | Puertos (interfaces ABC) definen contratos; los adaptadores implementan los detalles concretos |
| **Escalabilidad**   | Cada servicio puede escalar de forma independiente gracias al broker de eventos |
| **Arquitectura Hexagonal** | El dominio (models + services) no depende de infraestructura externa |
| **Event-Driven**     | El flujo completo se orquesta mediante eventos publicados y consumidos asíncronamente |
