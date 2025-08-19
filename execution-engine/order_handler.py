"""Order handler v0.2.0 (2025-08-19)"""

import json
import logging
from pathlib import Path
from typing import Dict

import psycopg2
import redis

from config import settings
from .adapters import IBKRAdapter, BinanceAdapter, BrokerAdapter


class OrderHandler:
    """Broker-agnostic order handler."""

    def __init__(
        self,
        log_path: str = "execution-engine/logs/orders.log",
        redis_client: redis.Redis | None = None,
    ) -> None:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("order_handler")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.adapters: Dict[str, BrokerAdapter] = {
            "ibkr": IBKRAdapter(),
            "binance": BinanceAdapter(),
        }
        self.redis = redis_client or redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )

    def place_order(self, broker: str, order: Dict) -> str:
        adapter = self.adapters[broker.lower()]
        result = adapter.place_order(order)
        log_entry = {"broker": broker, "order_id": result["order_id"], "order": order}
        self.logger.info(json.dumps(log_entry))
        self.redis.set(f"order:{result['order_id']}", json.dumps(result))
        try:
            with psycopg2.connect(
                host=settings.db_host,
                port=settings.db_port,
                dbname=settings.db_name,
                user=settings.db_user,
                password=settings.db_pass,
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO orders (account_id, symbol, side, qty, type, limit_price, status, reason, sl, tp)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING id
                        """,
                        (
                            order.get("account_id"),
                            order.get("symbol"),
                            order.get("side"),
                            order.get("qty"),
                            order.get("type"),
                            order.get("limit_price"),
                            order.get("status"),
                            order.get("reason"),
                            order.get("sl"),
                            order.get("tp"),
                        ),
                    )
                    db_order_id = cur.fetchone()[0]
                    if result.get("price") and result.get("qty"):
                        cur.execute(
                            """
                            INSERT INTO executions (order_id, price, qty, fee, ts)
                            VALUES (%s,%s,%s,%s,NOW())
                            """,
                            (
                                db_order_id,
                                result.get("price"),
                                result.get("qty"),
                                result.get("fee"),
                            ),
                        )
        except Exception as exc:  # pragma: no cover - database issues
            raise RuntimeError(f"Failed to persist order: {exc}") from exc
        return result["order_id"]
