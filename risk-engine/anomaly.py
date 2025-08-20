#!/usr/bin/env python3
"""Anomaly detection for daily risk metrics v0.1.0 (2025-08-20)"""
from __future__ import annotations

__version__ = "0.1.0"

import argparse
import os
import subprocess  # nosec B404

import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest

from common.monitoring import setup_logging
from config import settings
from messaging import EventProducer

logger = setup_logging(
    "risk-anomaly",
    log_path=os.path.join("logs", "risk-anomaly.log"),
    remote_url=settings.remote_log_url,
)


def detect_anomalies() -> int:
    """Detect anomalies from metrics_daily and store them."""
    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    )
    df = pd.read_sql(
        "SELECT date, portfolio_id, nav, ret, vol, dd, var95, es97 FROM metrics_daily",
        conn,
    )
    if df.empty:
        conn.close()
        logger.info("No metrics to evaluate")
        return 0
    features = df[["nav", "ret", "vol", "dd", "var95", "es97"]]
    model = IsolationForest(contamination=0.01, random_state=42)
    df["score"] = model.decision_function(features)
    df["anomaly"] = model.fit_predict(features)
    anomalies = df[df["anomaly"] == -1]

    cur = conn.cursor()
    for _, row in anomalies.iterrows():
        cur.execute(
            """
            INSERT INTO risk_anomalies (metric_date, portfolio_id, metric, value, score)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row["date"], int(row["portfolio_id"]), "nav", float(row["nav"]), float(row["score"])),
        )
    conn.commit()
    cur.close()
    conn.close()

    count = len(anomalies)
    if count:
        producer = EventProducer(settings.rabbitmq_url)
        producer.publish("risk_anomaly", {"count": count})
        producer.close()
        logger.info("Anomalies detected", extra={"count": count})
    else:
        logger.info("No anomalies detected")
    return count


def install_service() -> None:
    script_path = os.path.join(os.path.dirname(__file__), "install.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def remove_service() -> None:
    script_path = os.path.join(os.path.dirname(__file__), "remove.sh")
    subprocess.run([script_path], check=True)  # nosec B603


def main() -> None:
    parser = argparse.ArgumentParser(description="risk-anomaly detector v0.1.0")
    parser.add_argument("--install", action="store_true", help="Install risk-engine service")
    parser.add_argument("--remove", action="store_true", help="Remove risk-engine service")
    args = parser.parse_args()
    if args.install:
        install_service()
        return
    if args.remove:
        remove_service()
        return
    detect_anomalies()


if __name__ == "__main__":
    main()
