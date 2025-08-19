"""Base adapter interface v0.2.0 (2025-08-19)"""

from typing import Dict, Protocol


class BrokerAdapter(Protocol):
    """Adapter interface for brokers."""

    def place_order(self, order: Dict) -> Dict:
        """Place an order and return broker-specific details."""
        ...
