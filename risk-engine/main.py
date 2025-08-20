#!/usr/bin/env python3
"""risk-engine service v0.4.5 (2025-08-19)"""

import argparse
import json
import os
import subprocess  # nosec B404
from typing import List

import psycopg2
from fastapi import FastAPI, Request
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings
from messaging import EventConsumer
from engine import volatility_target
from stress_tests import historical_scenario, hypothetical_scenario

app = FastAPI(title="risk-engine", version="0.3.1")
logger = setup_logging("risk-engine", remote_url=settings.remote_log_url)
REQUEST_COUNT = setup_metrics("risk-engine", port=settings.risk_engine_metrics_port)
tracer = setup_tracer("risk-engine")


@app.middleware("http")
async def add_version_header(request: Request, call_next):
    with tracer.start_as_current_span(request.url.path):
        response = await call_next(request)
    REQUEST_COUNT.inc()
    response.headers["X-API-Version"] = "v0.3.1"
    return response


class StressRequest(BaseModel):
    prices: List[float]
    shocks: List[float]


class StressResponse(BaseModel):
    historical: List[float]
    hypothetical: List[float]


def _store_result(scenario: str, data: dict) -> None:
    try:
        with psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_pass,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO risk_stress_results (scenario, metric) VALUES (%s, %s)",
                    (scenario, json.dumps(data)),
                )
    except Exception as exc:  # pragma: no cover - log error path
        logger.error("DB insert failed: %s", exc)


@app.post("/risk/stress", response_model=StressResponse)
def stress(payload: StressRequest) -> StressResponse:
    historical = historical_scenario(payload.prices)
    hypothetical = hypothetical_scenario(payload.prices, payload.shocks)
    _store_result("historical", {"prices": payload.prices, "result": historical})
    _store_result("hypothetical", {"shocks": payload.shocks, "result": hypothetical})
    return StressResponse(historical=historical, hypothetical=hypothetical)


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
    parser = argparse.ArgumentParser(description="risk-engine consumer v0.4.5")
    parser.add_argument("--install", action="store_true", help="Install risk-engine service")
    parser.add_argument("--remove", action="store_true", help="Remove risk-engine service")
    parser.add_argument(
        "--log-path", default=os.path.join("logs", "risk-engine.log"), help="Path to log file"
    )
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
