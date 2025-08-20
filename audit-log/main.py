"""audit-log consumer v0.1.0 (2025-08-20)"""
import argparse
import json
import psycopg2
from messaging import EventConsumer
from common.monitoring import setup_logging
from config import settings

logger = setup_logging("audit-log", remote_url=settings.remote_log_url)

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
    logger.info("Logged %s", event)

def main() -> None:
    parser = argparse.ArgumentParser(description="audit-log consumer v0.1.0")
    parser.parse_args()
    consumer = EventConsumer(settings.rabbitmq_url, queue="audit-log")
    try:
        consumer.start(handle_event)
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
