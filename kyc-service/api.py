#!/usr/bin/env python3
"""kyc-service FastAPI app v0.1.1 (2025-08-20)"""
from __future__ import annotations

import json
from pathlib import Path
import os

from fastapi import FastAPI, UploadFile, File, Form

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings

__version__ = "0.1.1"

logger = setup_logging(
    "kyc-service",
    log_path="logs/kyc-service/kyc.log",
    remote_url=settings.remote_log_url,
)
REQUEST_COUNT = setup_metrics("kyc-service", port=settings.kyc_service_metrics_port)
tracer = setup_tracer("kyc-service")

app = FastAPI(title="kyc-service", version=__version__)

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
STATUS_FILE = UPLOAD_DIR / "status.json"


def load_statuses() -> dict[str, str]:
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text())
    return {}


def save_statuses(data: dict[str, str]) -> None:
    STATUS_FILE.write_text(json.dumps(data))


@app.post("/kyc/upload")
async def upload_document(user_id: int = Form(...), document: UploadFile = File(...)) -> dict[str, str]:
    with tracer.start_as_current_span("upload"):
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        file_path = UPLOAD_DIR / f"{user_id}_{document.filename}"
        file_path.write_bytes(await document.read())
        statuses = load_statuses()
        statuses[str(user_id)] = "pending"
        save_statuses(statuses)
        logger.info("Uploaded document", extra={"user_id": user_id})
        REQUEST_COUNT.inc()
    return {"status": "uploaded"}


@app.get("/kyc/status/{user_id}")
def get_status(user_id: int) -> dict[str, str]:
    with tracer.start_as_current_span("status"):
        statuses = load_statuses()
        status = statuses.get(str(user_id), "not_found")
        logger.info("Checked status", extra={"user_id": user_id, "status": status})
        REQUEST_COUNT.inc()
    return {"status": status}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("KYC_HOST", "127.0.0.1")
    port = int("8000")
    uvicorn.run("kyc-service.api:app", host=host, port=port)
