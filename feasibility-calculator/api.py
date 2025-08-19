"""FastAPI endpoint for feasibility analysis v0.1.1 (2025-08-19)"""
from __future__ import annotations

from datetime import datetime, date
from math import pow

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from common.monitoring import setup_logging, setup_metrics, setup_tracer
from config import settings

__version__ = "0.1.1"

app = FastAPI(title="feasibility-calculator", version=__version__)
logger = setup_logging("feasibility-calculator", remote_url=settings.remote_log_url)
REQUEST_COUNT = setup_metrics("feasibility-calculator", port=9003)
tracer = setup_tracer("feasibility-calculator")


class FeasibilityRequest(BaseModel):
    capital: float
    target: float
    deadline: date
    risk_profile: str


class FeasibilityResponse(BaseModel):
    cagr: float
    daily_return: float
    poh: float


RISK_PROFILE_POH = {
    "conservative": 0.5,
    "balanced": 0.7,
    "aggressive": 0.9,
}


@app.middleware("http")
async def observability_middleware(request, call_next):
    with tracer.start_as_current_span(request.url.path):
        response = await call_next(request)
    REQUEST_COUNT.inc()
    return response


@app.post("/feasibility", response_model=FeasibilityResponse)
def calculate(payload: FeasibilityRequest) -> FeasibilityResponse:
    today = datetime.utcnow().date()
    days = (payload.deadline - today).days
    if days <= 0:
        raise HTTPException(status_code=400, detail="Deadline must be in the future")
    years = days / 365
    growth = payload.target / payload.capital
    cagr = pow(growth, 1 / years) - 1
    daily_return = pow(growth, 1 / days) - 1
    poh = RISK_PROFILE_POH.get(payload.risk_profile.lower(), 0.0)
    logger.info("Calculated feasibility", extra={"cagr": cagr, "daily_return": daily_return, "poh": poh})
    return FeasibilityResponse(cagr=cagr, daily_return=daily_return, poh=poh)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("feasibility-calculator.api:app", host="127.0.0.1", port=8000)
