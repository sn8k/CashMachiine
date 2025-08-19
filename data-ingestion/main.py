#!/usr/bin/env python3
"""data-ingestion consumer v0.5.2 (2025-08-19)"""
import argparse
import os
import subprocess  # nosec B404

from common.monitoring import setup_logging
from config import settings
from messaging import EventConsumer
from fetchers.equities_yahoo import YahooEquityFetcher


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def handle_event(message: dict) -> None:
    event = message.get("event")
    if event == "data_fetch":
        symbol = message.get("payload", {}).get("symbol", "AAPL")
        fetcher = YahooEquityFetcher()
        fetcher.save(fetcher.fetch(symbol))
        logger.info("Fetched data for %s", symbol)


def main():
    parser = argparse.ArgumentParser(description="data-ingestion consumer v0.5.2")
    parser.add_argument("--install", action="store_true", help="Install data-ingestion service")
    parser.add_argument("--remove", action="store_true", help="Remove data-ingestion service")
    parser.add_argument("--log-path", default=os.path.join("logs", "data-ingestion.log"), help="Path to log file")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger
    logger = setup_logging("data-ingestion", log_path=args.log_path, remote_url=settings.remote_log_url)

    consumer = EventConsumer(settings.rabbitmq_url, queue="data-ingestion")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
