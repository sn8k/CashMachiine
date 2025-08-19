"""IBKR adapter v0.2.0 (2025-08-19)"""

from typing import Dict
import requests

from config import settings
from .base import BrokerAdapter


class IBKRAdapter:
    """Interactive Brokers adapter."""

    def __init__(self, base_url: str = "https://paper-api.interactivebrokers.com") -> None:
        self.base_url = base_url
        self.api_key = settings.ibkr_api_key

    def place_order(self, order: Dict) -> Dict:
        """Place an order via IBKR REST API."""
        try:
            resp = requests.post(
                f"{self.base_url}/v1/orders",
                headers={"IBKR-APIKEY": self.api_key},
                json=order,
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "order_id": str(data.get("id")),
                "price": data.get("price"),
                "qty": data.get("qty"),
            }
        except requests.RequestException as exc:  # pragma: no cover - network errors
            raise RuntimeError(f"IBKR order failed: {exc}") from exc
