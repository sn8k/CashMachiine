"""Risk-engine REST client v0.1.1 (2025-08-19)"""
import requests

from config import settings

__version__ = "0.1.1"


def adjust_risk(
    weights,
    returns,
    current_vol,
    target_vol,
    var_limit,
    es_limit,
    confidence,
    edge,
    variance,
    kelly_cap,
    url: str = settings.risk_engine_url
):
    """Call risk-engine `/adjust` endpoint and return JSON response."""
    payload = {
        "weights": list(weights),
        "returns": list(returns),
        "current_vol": current_vol,
        "target_vol": target_vol,
        "var_limit": var_limit,
        "es_limit": es_limit,
        "confidence": confidence,
        "edge": edge,
        "variance": variance,
        "kelly_cap": kelly_cap,
    }
    resp = requests.post(f"{url}/adjust", json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()
