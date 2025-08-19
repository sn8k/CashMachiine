"""Stress test utilities v0.1.0 (2025-08-19)"""
from __future__ import annotations
from typing import List
import numpy as np


def historical_scenario(prices: List[float]) -> List[float]:
    """Apply worst historical return to all prices."""
    if len(prices) < 2:
        return prices
    returns = np.diff(prices) / np.array(prices[:-1])
    shock = returns.min()
    return [p * (1 + shock) for p in prices]


def hypothetical_scenario(prices: List[float], shocks: List[float]) -> List[float]:
    """Apply provided shocks to prices element-wise."""
    if len(prices) != len(shocks):
        raise ValueError("prices and shocks must be same length")
    return [p * (1 + s) for p, s in zip(prices, shocks)]
