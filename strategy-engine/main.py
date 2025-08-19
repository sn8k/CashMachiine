#!/usr/bin/env python3
"""strategy-engine consumer v0.4.0 (2025-08-19)"""
import argparse
import os
import subprocess

from common.monitoring import setup_logging
from config import settings
from messaging import EventConsumer
from strategy-engine.strategies.core import CoreStrategy


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)


def handle_event(message: dict) -> None:
    if message.get("event") == "strategy_compute":
        strategy = CoreStrategy()
        signals = strategy.signals([])
        weights = strategy.target_weights(signals)
        logger.info("Computed strategy weights %s", weights)


def main():
    parser = argparse.ArgumentParser(description="strategy-engine consumer v0.4.0")
    parser.add_argument("--install", action="store_true", help="Install strategy-engine service")
    parser.add_argument("--remove", action="store_true", help="Remove strategy-engine service")
    parser.add_argument("--log-path", default=os.path.join("logs", "strategy-engine.log"), help="Path to log file")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger
    logger = setup_logging("strategy-engine", log_path=args.log_path, remote_url=settings.remote_log_url)

    consumer = EventConsumer(settings.rabbitmq_url, queue="strategy-engine")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
