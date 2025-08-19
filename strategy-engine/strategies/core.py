"""Core strategy example v0.1.2 (2025-08-20)"""
from strategy_engine.interface import Strategy
from strategy_engine.risk_client import adjust_risk
from common.monitoring import setup_performance_metrics

__version__ = "0.1.2"

SIGNAL_LATENCY = setup_performance_metrics("strategy-engine-core")


class CoreStrategy(Strategy):
    """Long-term core allocation example with risk adjustment."""

    def __init__(self):
        self._last_explanation = ""

    def signals(self, market_data):
        with SIGNAL_LATENCY.time():
            price = market_data.get("SPY", {}).get("close", 0)
            prev = market_data.get("SPY", {}).get("prev_close", price)
            ret = (price - prev) / prev if prev else 0.0
            return {"SPY": ret}

    def target_weights(self, signals):
        raw = 1.0 if signals.get("SPY", 0) > 0 else 0.0
        result = adjust_risk(
            weights=[raw],
            returns=[signals.get("SPY", 0)],
            current_vol=0.2,
            target_vol=0.1,
            var_limit=0.05,
            es_limit=0.1,
            confidence=0.95,
            edge=signals.get("SPY", 0),
            variance=signals.get("SPY", 0) ** 2,
            kelly_cap=0.5,
        )
        self._last_explanation = result.get("explanation", "")
        adjusted = result.get("weights", [raw])[0]
        return {"SPY": adjusted}

    def explain(self) -> str:
        return self._last_explanation or "No explanation available."
