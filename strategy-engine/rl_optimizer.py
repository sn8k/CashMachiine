"""Reinforcement learning optimizer utilities v0.1.1 (2025-08-20)"""
import numpy as np

__version__ = "0.1.1"

def optimize_allocation(recent_return: float) -> float:
    """Return a simple allocation proportionate to the latest return.

    Positive returns increase allocation, negative returns decrease it,
    bounded between 0 and 1.
    """
    return float(np.clip(0.5 + recent_return, 0.0, 1.0))
