#!/usr/bin/env python3
"""whatif-service FastAPI app v0.3.1 (2025-08-20)"""
from __future__ import annotations

import os
from typing import Any

import psycopg2
from psycopg2.extras import Json, RealDictCursor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings

__version__ = "0.3.1"

app = FastAPI(title="whatif-service", version=__version__)
logger = setup_logging(
    "whatif-service",
    log_path="logs/whatif-service/whatif.log",
    remote_url=settings.remote_log_url,
)
REQUEST_COUNT = setup_metrics("whatif-service", port=9009)
tracer = setup_tracer("whatif-service")


class ScenarioRunRequest(BaseModel):
    name: str
    params: dict[str, Any] = {}


class ScenarioRunResponse(BaseModel):
    id: int


class ScenarioResult(BaseModel):
    id: int
    name: str
    result: dict[str, Any]


def _conn() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_pass,
    )


@app.post("/scenarios/run", response_model=ScenarioRunResponse)
def run_scenario(payload: ScenarioRunRequest) -> ScenarioRunResponse:
    with tracer.start_as_current_span("run-scenario"):
        result = {"status": "ok", "params": payload.params}
        conn = _conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO scenario_results (name, input, result)
                    VALUES (%s, %s, %s) RETURNING id""",
                    (payload.name, Json(payload.params), Json(result)),
                )
                scenario_id = cur.fetchone()[0]
        conn.close()
        logger.info("Ran scenario", extra={"id": scenario_id, "name": payload.name})
        REQUEST_COUNT.inc()
    return ScenarioRunResponse(id=scenario_id)


@app.get("/scenarios/{scenario_id}", response_model=ScenarioResult)
def get_scenario(scenario_id: int) -> ScenarioResult:
    with tracer.start_as_current_span("get-scenario"):
        conn = _conn()
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, result FROM scenario_results WHERE id=%s",
                    (scenario_id,),
                )
                row = cur.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Scenario not found")
        logger.info("Fetched scenario", extra={"id": scenario_id})
        REQUEST_COUNT.inc()
    return ScenarioResult(id=row["id"], name=row["name"], result=row["result"])


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("WHATIF_HOST", "127.0.0.1")
    port = int(os.getenv("WHATIF_PORT", "8000"))
    uvicorn.run("whatif-service.api:app", host=host, port=port)
