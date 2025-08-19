#!/usr/bin/env python3
"""notification-service FastAPI app v0.3.1 (2025-08-19)"""
from __future__ import annotations

import os
import threading
from typing import Any

import psycopg2
from psycopg2.extras import Json
from fastapi import FastAPI
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings
from messaging import EventConsumer

__version__ = "0.3.1"

logger = setup_logging(
    "notification-service",
    log_path="logs/notification-service/notification.log",
    remote_url=settings.remote_log_url,
)
REQUEST_COUNT = setup_metrics("notification-service", port=settings.notification_service_metrics_port)
tracer = setup_tracer("notification-service")

app = FastAPI(title="notification-service", version=__version__)


class EmailNotification(BaseModel):
    user_id: int
    to: str
    subject: str
    body: str


class WebhookNotification(BaseModel):
    user_id: int
    url: str
    payload: dict[str, Any]


def save_notification(channel: str, payload: dict[str, Any]) -> None:
    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO notifications (user_id, channel, payload) VALUES (%s, %s, %s)""",
                (payload.get("user_id", 0), channel, Json(payload)),
            )
    conn.close()


@app.post("/notify/email")
def notify_email(note: EmailNotification) -> dict[str, str]:
    with tracer.start_as_current_span("notify-email"):
        save_notification("email", note.dict())
        logger.info("Queued email notification", extra={"to": note.to})
        REQUEST_COUNT.inc()
    return {"status": "queued"}


@app.post("/notify/webhook")
def notify_webhook(note: WebhookNotification) -> dict[str, str]:
    with tracer.start_as_current_span("notify-webhook"):
        save_notification("webhook", note.dict())
        logger.info("Queued webhook notification", extra={"url": note.url})
        REQUEST_COUNT.inc()
    return {"status": "queued"}


def handle_event(message: dict[str, Any]) -> None:
    channel = message.get("channel", "email")
    payload = message.get("payload", {})
    with tracer.start_as_current_span(f"event-{channel}"):
        save_notification(channel, payload)
        logger.info("Processed event notification", extra={"channel": channel})
        REQUEST_COUNT.inc()


def start_consumer() -> None:
    consumer = EventConsumer(settings.rabbitmq_url, queue="notifications")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()


@app.on_event("startup")
def startup() -> None:
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("NOTIFICATION_HOST", "127.0.0.1")
    port = int(os.getenv("NOTIFICATION_PORT", "8000"))
    uvicorn.run("notification-service.api:app", host=host, port=port)
