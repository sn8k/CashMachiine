#!/usr/bin/env python3
"""orchestrator scheduler v0.4.0 (2025-08-19)"""
import argparse
import os
import subprocess
import time
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings
from messaging import EventProducer


tracer = setup_tracer("orchestrator")


def sample_job(producer: EventProducer):
    with tracer.start_as_current_span("sample_job"):
        JOB_COUNTER.inc()
        logger.info("Orchestrator job executed")
        producer.publish("fetch_equities", {"symbol": "AAPL"})


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)


def main():
    parser = argparse.ArgumentParser(description="Orchestrator controller v0.4.0")
    parser.add_argument("--install", action="store_true", help="Install orchestrator service")
    parser.add_argument("--remove", action="store_true", help="Remove orchestrator service")
    parser.add_argument("--log-path", default=os.path.join("logs", "orchestrator.log"), help="Path to log file")
    parser.add_argument("--metrics-port", type=int, default=9000, help="Prometheus metrics port")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    global logger, JOB_COUNTER
    logger = setup_logging("orchestrator", log_path=args.log_path, remote_url=settings.remote_log_url)
    JOB_COUNTER = setup_metrics("orchestrator", port=args.metrics_port)

    producer = EventProducer(settings.rabbitmq_url)
    scheduler = BackgroundScheduler(timezone=ZoneInfo("Europe/Paris"))
    scheduler.add_job(sample_job, "cron", hour=8, minute=0, args=[producer])
    scheduler.start()
    logger.info("Scheduler started, waiting for jobs")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        producer.close()


if __name__ == "__main__":
    main()
