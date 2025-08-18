"""IBKR adapter v0.1.0"""

from typing import Dict

from .base import BrokerAdapter

class IBKRAdapter:
    """Interactive Brokers adapter."""
    def place_order(self, order: Dict) -> str:  # pragma: no cover - placeholder
        return "IBKR_ORDER_ID"
