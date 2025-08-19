"""Satellite strategy example v0.1.3 (2025-08-19)"""
from strategy_engine.interface import Strategy
from strategy_engine.risk_client import adjust_risk
from strategy_engine.ml_forecast import forecast_prices
from common.monitoring import setup_performance_metrics

__version__ = "0.1.3"

SIGNAL_LATENCY = setup_performance_metrics("strategy-engine-satellite")


class SatelliteStrategy(Strategy):
    """Tactical satellite allocation example with risk adjustment."""

    def __init__(self):
        self._last_explanation = ""

    def signals(self, market_data):
        with SIGNAL_LATENCY.time():
            symbol = "BTC"
            price = market_data.get(symbol, {}).get("close", 0)
            history = market_data.get(symbol, {}).get("history", [])
            forecast = forecast_prices(symbol, history + [price])
            ret = (forecast - price) / price if price else 0.0
            return {symbol: ret}

    def target_weights(self, signals):
        raw = 0.1 if signals.get("BTC", 0) > 0 else 0.0
        result = adjust_risk(
            weights=[raw],
            returns=[signals.get("BTC", 0)],
            current_vol=0.8,
            target_vol=0.5,
            var_limit=0.2,
            es_limit=0.3,
            confidence=0.95,
            edge=signals.get("BTC", 0),
            variance=signals.get("BTC", 0) ** 2,
            kelly_cap=0.5,
        )
        self._last_explanation = result.get("explanation", "")
        adjusted = result.get("weights", [raw])[0]
        return {"BTC": adjusted}

    def explain(self) -> str:
        return self._last_explanation or "No explanation available."
