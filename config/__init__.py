"""Configuration loader v0.1.3 (2025-08-19)"""
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    secret_key: str = os.getenv("SECRET_KEY", "secret")
    remote_log_url: str | None = os.getenv("REMOTE_LOG_URL")
    api_gateway_metrics_port: int = int(os.getenv("API_GATEWAY_METRICS_PORT", "9001"))
    risk_engine_metrics_port: int = int(os.getenv("RISK_ENGINE_METRICS_PORT", "9002"))
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "cashmachiine")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_pass: str = os.getenv("DB_PASS", "")
    risk_engine_url: str = os.getenv("RISK_ENGINE_URL", "http://localhost:8000")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    alpha_vantage_key: str = os.getenv("ALPHA_VANTAGE_KEY", "demo")


settings = Settings()
