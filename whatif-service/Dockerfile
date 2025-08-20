# Dockerfile v0.3.1 (2025-08-20)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt
COPY . .
CMD ["uvicorn", "whatif-service.api:app", "--host", "0.0.0.0", "--port", "8000"]
