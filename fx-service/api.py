#!/usr/bin/env python3
"""fx-service FastAPI app v0.1.0 (2025-08-19)"""
from __future__ import annotations

import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings

__version__ = "0.1.0"

app = FastAPI(title="fx-service", version=__version__)
logger = setup_logging(
    "fx-service",
    log_path="logs/fx-service/fx.log",
    remote_url=settings.remote_log_url,
)
REQUEST_COUNT = setup_metrics("fx-service", port=9004)
tracer = setup_tracer("fx-service")

ECB_URL = "https://api.exchangerate.host/latest"

class ConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class ConversionResponse(BaseModel):
    rate: float
    converted: float

def fetch_rate(from_currency: str, to_currency: str) -> float:
    response = requests.get(
        ECB_URL,
        params={"base": from_currency.upper(), "symbols": to_currency.upper()},
        timeout=5,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch rates")
    data = response.json()
    rate = data["rates"].get(to_currency.upper())
    if rate is None:
        raise HTTPException(status_code=400, detail="Unsupported currency")
    return rate

@app.post("/convert", response_model=ConversionResponse)
def convert(payload: ConversionRequest) -> ConversionResponse:
    with tracer.start_as_current_span("convert"):
        rate = fetch_rate(payload.from_currency, payload.to_currency)
        converted = payload.amount * rate
        logger.info(
            "Converted currency",
            extra={
                "from": payload.from_currency,
                "to": payload.to_currency,
                "amount": payload.amount,
                "converted": converted,
            },
        )
        REQUEST_COUNT.inc()
    return ConversionResponse(rate=rate, converted=converted)

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("FX_HOST", "127.0.0.1")
    port = int(os.getenv("FX_PORT", "8000"))
    uvicorn.run("fx-service.api:app", host=host, port=port)
