#!/usr/bin/env python3
"""execution-engine consumer v0.4.3 (2025-08-19)"""
import argparse
import os
import subprocess  # nosec B404

from common.monitoring import setup_logging
from config import settings
from messaging import EventConsumer
from order_handler import OrderHandler


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def handle_event(message: dict) -> None:
    if message.get("event") == "order_dispatch":
        payload = message.get("payload", {})
        broker = payload.get("broker", "ibkr")
        order = {"symbol": payload.get("symbol", "AAPL"), "qty": payload.get("qty", 1)}
        handler = OrderHandler()
        order_id = handler.place_order(broker, order)
        logger.info("Dispatched order %s", order_id)


def main():
    parser = argparse.ArgumentParser(description="execution-engine consumer v0.4.3")
    parser.add_argument("--install", action="store_true", help="Install execution-engine service")
    parser.add_argument("--remove", action="store_true", help="Remove execution-engine service")
    parser.add_argument("--log-path", default=os.path.join("logs", "execution-engine.log"), help="Path to log file")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger
    logger = setup_logging("execution-engine", log_path=args.log_path, remote_url=settings.remote_log_url)

    consumer = EventConsumer(settings.rabbitmq_url, queue="execution-engine")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
