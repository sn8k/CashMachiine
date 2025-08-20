"""Configuration loader v0.1.11 (2025-08-20)"""
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
    execution_engine_metrics_port: int = int(os.getenv("EXECUTION_ENGINE_METRICS_PORT", "9003"))
    data_ingestion_metrics_port: int = int(os.getenv("DATA_INGESTION_METRICS_PORT", "9004"))
    backtester_metrics_port: int = int(os.getenv("BACKTESTER_METRICS_PORT", "9005"))
    notification_service_metrics_port: int = int(os.getenv("NOTIFICATION_SERVICE_METRICS_PORT", "9006"))
    alert_engine_metrics_port: int = int(os.getenv("ALERT_ENGINE_METRICS_PORT", "9009"))
    strategy_marketplace_metrics_port: int = int(os.getenv("STRATEGY_MARKETPLACE_METRICS_PORT", "9007"))
    kyc_service_metrics_port: int = int(os.getenv("KYC_SERVICE_METRICS_PORT", "9008"))
    macro_service_metrics_port: int = int(os.getenv("MACRO_SERVICE_METRICS_PORT", "9010"))
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "cashmachiine")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_pass: str = os.getenv("DB_PASS", "")
    risk_engine_url: str = os.getenv("RISK_ENGINE_URL", "http://localhost:8000")
    notification_service_url: str = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8200")
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    alpha_vantage_key: str = os.getenv("ALPHA_VANTAGE_KEY", "demo")
    binance_api_key: str = os.getenv("BINANCE_API_KEY", "demo")
    binance_api_secret: str = os.getenv("BINANCE_API_SECRET", "demo")
    ibkr_api_key: str = os.getenv("IBKR_API_KEY", "demo")
    fred_api_key: str = os.getenv("FRED_API_KEY", "demo")
    kyc_service_url: str = os.getenv("KYC_SERVICE_URL", "http://localhost:8400")
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    google_token_url: str = os.getenv(
        "GOOGLE_TOKEN_URL", "https://oauth2.googleapis.com/token"
    )
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    github_token_url: str = os.getenv(
        "GITHUB_TOKEN_URL", "https://github.com/login/oauth/access_token"
    )


settings = Settings()
