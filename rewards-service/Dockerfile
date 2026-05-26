FROM python:3.11-slim

WORKDIR /app

COPY rewards-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY rewards-service/ .

ENV PYTHONPATH="/app"

CMD ["python", "main.py"]
