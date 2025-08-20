# Dockerfile v0.1.0 (2025-08-20)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore -r requirements.txt
COPY . .
CMD ["python", "audit-log/main.py"]
