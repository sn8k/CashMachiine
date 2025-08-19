"""Binance adapter v0.2.0 (2025-08-19)"""

from typing import Dict
import requests

from config import settings
from .base import BrokerAdapter


class BinanceAdapter:
    """Binance adapter."""

    def __init__(self, base_url: str = "https://api.binance.com") -> None:
        self.base_url = base_url
        self.api_key = settings.binance_api_key

    def place_order(self, order: Dict) -> Dict:
        """Place an order via Binance REST API."""
        try:
            resp = requests.post(
                f"{self.base_url}/api/v3/order",
                headers={"X-MBX-APIKEY": self.api_key},
                json=order,
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "order_id": str(data.get("orderId")),
                "price": data.get("fills", [{}])[0].get("price"),
                "qty": data.get("executedQty"),
            }
        except requests.RequestException as exc:  # pragma: no cover - network errors
            raise RuntimeError(f"Binance order failed: {exc}") from exc
