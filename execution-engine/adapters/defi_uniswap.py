"""Uniswap DeFi adapter v0.1.0 (2025-08-20)"""
from typing import Dict
from web3 import Web3

from .base import BrokerAdapter


class UniswapAdapter:
    """Adapter for executing swaps via Uniswap."""

    def __init__(self, provider_url: str = "http://localhost:8545") -> None:
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

    def place_order(self, order: Dict) -> Dict:
        """Broadcast a signed swap transaction and return its receipt."""
        try:
            tx_hash = self.w3.eth.send_raw_transaction(order["raw_tx"])
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            return {"tx_hash": tx_hash.hex(), "status": receipt.status}
        except Exception as exc:  # pragma: no cover - network errors
            raise RuntimeError(f"Uniswap trade failed: {exc}") from exc
