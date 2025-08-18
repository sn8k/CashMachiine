"""Binance adapter v0.1.0"""

from typing import Dict

from .base import BrokerAdapter

class BinanceAdapter:
    """Binance adapter."""
    def place_order(self, order: Dict) -> str:  # pragma: no cover - placeholder
        return "BINANCE_ORDER_ID"
