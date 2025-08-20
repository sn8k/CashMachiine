#!/usr/bin/env python3
"""orchestrator scheduler v0.5.7 (2025-08-20)"""
import argparse
import os
import subprocess  # nosec B404
import time
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
import random

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings
from messaging import EventProducer


SECURE_RANDOM = random.SystemRandom()


tracer = setup_tracer("orchestrator")


def run_pipeline(producer: EventProducer):
    """Dispatch sequential service events."""
    with tracer.start_as_current_span("run_pipeline"):
        JOB_COUNTER.inc()
        logger.info("Starting pipeline dispatch")
        producer.publish("data_fetch", {"symbol": "AAPL", "asset_class": "equity"})
        producer.publish("data_fetch", {"symbol": "US10Y", "asset_class": "bond"})
        producer.publish("data_fetch", {"symbol": "GC=F", "asset_class": "commodity"})
        producer.publish("strategy_compute", {})
        producer.publish("risk_adjust", {"weights": [1.0], "current_vol": 0.05, "target_vol": 0.1})
        producer.publish(
            "order_dispatch",
            {"broker": "ibkr", "symbol": "AAPL", "qty": 10, "tenant_id": 1},
        )
        logger.info("Pipeline events emitted")


def _current_volatility() -> float:
    return SECURE_RANDOM.uniform(0, 0.1)


def _current_drawdown() -> float:
    return SECURE_RANDOM.uniform(-0.1, 0)


def check_intraday(producer: EventProducer):
    """Emit alerts when intraday thresholds are breached."""
    with tracer.start_as_current_span("check_intraday"):
        vol = _current_volatility()
        dd = _current_drawdown()
        if vol > settings.intraday_vol_threshold:
            payload = {"current_vol": vol, "threshold": settings.intraday_vol_threshold, "tenant_id": 1}
            producer.publish("volatility_alert", payload)
            logger.warning("Volatility threshold breached %.4f", vol)
        if dd <= -settings.intraday_drawdown_threshold:
            payload = {"current_drawdown": dd, "threshold": settings.intraday_drawdown_threshold, "tenant_id": 1}
            producer.publish("drawdown_alert", payload)
            logger.warning("Drawdown threshold breached %.4f", dd)


def run_db_backup():
    """Trigger database backup script."""
    with tracer.start_as_current_span("run_db_backup"):
        script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "db_backup.sh"))
        subprocess.run([script], check=True)  # nosec B603
        logger.info("Database backup completed")


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def main():
    parser = argparse.ArgumentParser(description="Orchestrator controller v0.5.7")
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
    scheduler.add_job(run_pipeline, "cron", hour=8, minute=0, args=[producer])
    scheduler.add_job(run_db_backup, "cron", hour=2, minute=0)
    scheduler.add_job(check_intraday, "interval", minutes=5, args=[producer])
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
