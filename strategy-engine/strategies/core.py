"""Core strategy example v0.1.1 (2025-08-19)"""
from ..interface import Strategy
from common.monitoring import setup_performance_metrics

__version__ = "0.1.1"

SIGNAL_LATENCY = setup_performance_metrics("strategy-engine-core")


class CoreStrategy(Strategy):
    """Long-term core allocation example."""

    def signals(self, market_data):
        with SIGNAL_LATENCY.time():
            return {"SPY": 1.0}

    def target_weights(self, signals):
        return {"SPY": 1.0}
