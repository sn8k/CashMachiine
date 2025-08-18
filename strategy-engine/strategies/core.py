"""Core strategy example v0.1.0 (2025-08-18)"""
from ..interface import Strategy

__version__ = "0.1.0"


class CoreStrategy(Strategy):
    """Long-term core allocation example."""

    def signals(self, market_data):
        return {"SPY": 1.0}

    def target_weights(self, signals):
        return {"SPY": 1.0}
