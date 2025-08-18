"""FastAPI endpoint for risk adjustments v0.3.0 (2025-08-18)"""
from __future__ import annotations

__version__ = "0.3.0"

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

try:  # local import when executed as module
    from .engine import volatility_target, var_es, kelly_fraction
except Exception:  # fallback for direct execution
    from engine import volatility_target, var_es, kelly_fraction


class RiskRequest(BaseModel):
    weights: List[float]
    returns: List[float]
    current_vol: float
    target_vol: float
    var_limit: float
    es_limit: float
    confidence: float = 0.95
    edge: float
    variance: float
    kelly_cap: float


class RiskResponse(BaseModel):
    adjusted_weights: List[float]
    var: float
    es: float
    kelly_fraction: float


app = FastAPI(title="risk-engine", version=__version__)


@app.post("/adjust", response_model=RiskResponse)
def adjust(payload: RiskRequest) -> RiskResponse:
    adjusted = volatility_target(payload.weights, payload.current_vol, payload.target_vol)
    var, es = var_es(payload.returns, payload.confidence)
    kelly = kelly_fraction(payload.edge, payload.variance, payload.kelly_cap)
    if var > payload.var_limit or es > payload.es_limit:
        adjusted = [0.0 for _ in adjusted]
    return RiskResponse(adjusted_weights=adjusted, var=var, es=es, kelly_fraction=kelly)
