"""Base adapter interface v0.1.0"""

from typing import Dict, Protocol

class BrokerAdapter(Protocol):
    """Adapter interface for brokers."""
    def place_order(self, order: Dict) -> str:
        """Place an order and return broker-specific id."""
        ...
