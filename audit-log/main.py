"""audit-log consumer v0.1.1 (2025-08-20)"""
import argparse
import json
import os
import subprocess  # nosec B404

import psycopg2

from messaging import EventConsumer
from common.monitoring import setup_logging
from config import settings


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def handle_event(message: dict) -> None:
    event = message.get("event")
    payload = json.dumps(message.get("payload"))
    with psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO audit_events (event, payload, tenant_id) VALUES (%s,%s,%s)",
                (event, payload, message.get("payload", {}).get("tenant_id", 1)),
            )
            conn.commit()
    logger.info("Logged %s payload=%s", event, payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="audit-log consumer v0.1.1")
    parser.add_argument("--install", action="store_true", help="Install audit-log service")
    parser.add_argument("--remove", action="store_true", help="Remove audit-log service")
    parser.add_argument(
        "--log-path",
        default=os.path.join("logs", "audit-log", "audit.log"),
        help="Path to log file",
    )
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger
    logger = setup_logging("audit-log", log_path=args.log_path, remote_url=settings.remote_log_url)

    consumer = EventConsumer(settings.rabbitmq_url, queue="audit-log")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
