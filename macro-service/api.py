#!/usr/bin/env python3
"""macro-service FastAPI app v0.1.0 (2025-08-20)"""
from __future__ import annotations

import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings

__version__ = "0.1.0"

app = FastAPI(title="macro-service", version=__version__)
logger = setup_logging(
    "macro-service", log_path="logs/macro-service/macro.log", remote_url=settings.remote_log_url
)
REQUEST_COUNT = setup_metrics("macro-service", port=settings.macro_service_metrics_port)
tracer = setup_tracer("macro-service")


class Indicator(BaseModel):
    indicator: str
    source: str
    value: float
    ts: str


@app.get("/indicators/latest", response_model=list[Indicator])
def latest() -> list[Indicator]:
    with tracer.start_as_current_span("latest"):
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_pass,
        )
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT ON (indicator) indicator, source, value, ts
                FROM macro_indicators
                ORDER BY indicator, ts DESC
                """
            )
            rows = cur.fetchall()
        conn.close()
        REQUEST_COUNT.inc()
        return [Indicator(indicator=r[0], source=r[1], value=float(r[2]), ts=r[3].isoformat()) for r in rows]


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("MACRO_HOST", "127.0.0.1")
    port = int(os.getenv("MACRO_PORT", "8000"))
    uvicorn.run("macro-service.api:app", host=host, port=port)
