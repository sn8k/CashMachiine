# Dockerfile v0.1.0 (2025-08-19)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt
COPY . .
CMD ["uvicorn", "strategy-marketplace.api:app", "--host", "0.0.0.0", "--port", "8000"]
