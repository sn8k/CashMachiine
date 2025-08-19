#!/usr/bin/env python3
"""risk-engine consumer v0.4.2 (2025-08-19)"""
import argparse
import os
import subprocess  # nosec B404

from common.monitoring import setup_logging
from config import settings
from messaging import EventConsumer
from engine import volatility_target


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def handle_event(message: dict) -> None:
    if message.get("event") == "risk_adjust":
        payload = message.get("payload", {})
        weights = payload.get("weights", [1.0])
        current_vol = payload.get("current_vol", 1.0)
        target_vol = payload.get("target_vol", 1.0)
        adjusted = volatility_target(weights, current_vol, target_vol)
        logger.info("Adjusted weights %s", adjusted)


def main():
    parser = argparse.ArgumentParser(description="risk-engine consumer v0.4.2")
    parser.add_argument("--install", action="store_true", help="Install risk-engine service")
    parser.add_argument("--remove", action="store_true", help="Remove risk-engine service")
    parser.add_argument("--log-path", default=os.path.join("logs", "risk-engine.log"), help="Path to log file")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger
    logger = setup_logging("risk-engine", log_path=args.log_path, remote_url=settings.remote_log_url)

    consumer = EventConsumer(settings.rabbitmq_url, queue="risk-engine")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
