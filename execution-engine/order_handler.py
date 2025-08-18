"""Order handler v0.1.0"""

import json
import logging
from pathlib import Path
from typing import Dict

from .adapters import IBKRAdapter, BinanceAdapter, BrokerAdapter

class OrderHandler:
    """Broker-agnostic order handler."""
    def __init__(self, log_path: str = "execution-engine/logs/orders.log") -> None:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("order_handler")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.adapters: Dict[str, BrokerAdapter] = {
            "ibkr": IBKRAdapter(),
            "binance": BinanceAdapter(),
        }

    def place_order(self, broker: str, order: Dict) -> str:
        adapter = self.adapters[broker.lower()]
        order_id = adapter.place_order(order)
        log_entry = {"broker": broker, "order_id": order_id, "order": order}
        self.logger.info(json.dumps(log_entry))
        return order_id
