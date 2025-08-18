"""Risk calculation utilities v0.3.0 (2025-08-18)"""
from __future__ import annotations

__version__ = "0.3.0"

from typing import Iterable, List, Tuple


def volatility_target(weights: Iterable[float], current_vol: float, target_vol: float) -> List[float]:
    """Scale weights to meet target volatility."""
    if current_vol <= 0:
        return list(weights)
    scale = target_vol / current_vol
    return [w * scale for w in weights]


def var_es(returns: Iterable[float], confidence: float = 0.95) -> Tuple[float, float]:
    """Return Value-at-Risk and Expected Shortfall for given returns."""
    data = sorted(returns)
    n = len(data)
    if n == 0 or not 0 < confidence < 1:
        return 0.0, 0.0
    index = max(int((1 - confidence) * n) - 1, 0)
    var = abs(data[index])
    tail = [abs(r) for r in data[: index + 1]]
    es = sum(tail) / len(tail) if tail else var
    return var, es


def kelly_fraction(edge: float, variance: float, cap: float) -> float:
    """Return Kelly optimal fraction capped at `cap`."""
    if variance <= 0:
        return 0.0
    kelly = edge / variance
    return max(0.0, min(kelly, cap))
