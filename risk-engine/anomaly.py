#!/usr/bin/env python3
"""Risk metric anomaly detection v0.1.0 (2025-08-20)"""

import os
from typing import List, Tuple

import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest

from common.monitoring import setup_logging
from config import settings
from messaging import EventProducer

LOG_PATH = os.path.join("logs", "risk-engine", "anomaly.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logger = setup_logging("risk-engine", log_path=LOG_PATH, remote_url=settings.remote_log_url)

FEATURES = ["nav", "ret", "vol", "dd", "var95", "es97"]


def _fetch_metrics() -> pd.DataFrame:
    with psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    ) as conn:
        return pd.read_sql_query(
            "SELECT date, portfolio_id, nav, ret, vol, dd, var95, es97 FROM metrics_daily",
            conn,
        )


def _store_anomalies(rows: List[Tuple]) -> None:
    if not rows:
        return
    with psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    ) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO risk_anomalies (date, portfolio_id, metric, value, score) VALUES (%s,%s,%s,%s,%s)",
                rows,
            )


def detect_anomalies() -> None:
    df = _fetch_metrics()
    if df.empty:
        logger.info("No metrics available for anomaly detection")
        return
    producer = EventProducer(settings.rabbitmq_url)
    anomalies: List[Tuple] = []
    try:
        for metric in FEATURES:
            model = IsolationForest(contamination=0.05, random_state=42)
            values = df[[metric]].values
            if len(values) < 10:
                continue
            model.fit(values)
            preds = model.predict(values)
            scores = model.decision_function(values)
            for row, pred, score in zip(df.itertuples(index=False), preds, scores):
                if pred == -1:
                    anomalies.append(
                        (row.date, row.portfolio_id, metric, getattr(row, metric), float(score))
                    )
                    producer.publish(
                        "risk_metric", {"metric": f"{metric}_anomaly", "value": 1.0}
                    )
                    logger.warning(
                        "Anomaly detected",
                        extra={
                            "date": str(row.date),
                            "portfolio_id": row.portfolio_id,
                            "metric": metric,
                            "value": getattr(row, metric),
                            "score": float(score),
                        },
                    )
    finally:
        producer.close()
    _store_anomalies(anomalies)


if __name__ == "__main__":
    detect_anomalies()
