#!/usr/bin/env python3
"""orchestrator scheduler v0.3.0"""
import argparse
import logging
import os
import subprocess
import time
from logging.handlers import RotatingFileHandler
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler

LOG_DEFAULT = os.environ.get("ORCHESTRATOR_LOG", "orchestrator/logs/orchestrator.log")


def sample_job():
    logging.info("Orchestrator job executed")


def install_service():
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)


def remove_service():
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)


def main():
    parser = argparse.ArgumentParser(description="Orchestrator controller v0.3.0")
    parser.add_argument("--install", action="store_true", help="Install orchestrator service")
    parser.add_argument("--remove", action="store_true", help="Remove orchestrator service")
    parser.add_argument("--log-path", default=LOG_DEFAULT, help="Path to log file")
    args = parser.parse_args()

    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return

    log_path = args.log_path
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(level=logging.INFO,
                        handlers=[RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3),
                                  logging.StreamHandler()],
                        format="%(asctime)s %(levelname)s %(message)s")

    scheduler = BackgroundScheduler(timezone=ZoneInfo("Europe/Paris"))
    scheduler.add_job(sample_job, "cron", hour=8, minute=0)
    scheduler.start()
    logging.info("Scheduler started, waiting for jobs")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()
