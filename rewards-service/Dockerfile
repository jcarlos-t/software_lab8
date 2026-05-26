FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app

COPY rewards-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY rewards-service/ .

RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH="/app"

CMD ["python", "main.py"]
