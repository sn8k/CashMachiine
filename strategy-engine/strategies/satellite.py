"""Satellite strategy example v0.1.0 (2025-08-18)"""
from ..interface import Strategy

__version__ = "0.1.0"


class SatelliteStrategy(Strategy):
    """Tactical satellite allocation example."""

    def signals(self, market_data):
        return {"BTC": 0.5}

    def target_weights(self, signals):
        return {"BTC": 0.1}
