#!/usr/bin/env python3
"""alert-engine service v0.1.0 (2025-08-20)"""

import argparse
import os
import subprocess  # nosec B404
import requests
from typing import Dict

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings
from messaging import EventConsumer

logger = setup_logging("alert-engine", remote_url=settings.remote_log_url)
REQUEST_COUNT = setup_metrics("alert-engine", port=settings.alert_engine_metrics_port)
tracer = setup_tracer("alert-engine")

THRESHOLD = 0.9


def _send_alert(message: str) -> None:
    try:
        requests.post(
            f"{settings.notification_service_url}/notify/webhook",
            json={"message": message},
            timeout=5,
        )
        logger.info("Alert sent", extra={"message": message})
    except requests.RequestException as exc:  # pragma: no cover - log error path
        logger.error("Notification failed", extra={"error": str(exc)})


def process_metric(payload: Dict[str, float]) -> None:
    value = payload.get("value", 0.0)
    metric = payload.get("metric", "")
    if value > THRESHOLD:
        _send_alert(f"{metric} threshold exceeded: {value}")


def handle_event(message: Dict) -> None:
    if message.get("event") == "risk_metric":
        process_metric(message.get("payload", {}))

def install_service() -> None:
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603

def remove_service() -> None:
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def main() -> None:
    parser = argparse.ArgumentParser(description="alert-engine consumer v0.1.0")
    parser.add_argument("--install", action="store_true", help="Install alert-engine service")
    parser.add_argument("--remove", action="store_true", help="Remove alert-engine service")
    parser.add_argument("--log-path", default=os.path.join("logs", "alert-engine", "alert.log"), help="Path to log file")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger
    logger = setup_logging("alert-engine", log_path=args.log_path, remote_url=settings.remote_log_url)

    consumer = EventConsumer(settings.rabbitmq_url, queue="risk-metrics")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
