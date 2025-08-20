"""Orders repository v0.1.2 (2025-08-20)"""
from psycopg2.extras import RealDictCursor
from . import get_connection


def fetch_orders_preview(limit: int = 10, tenant_id: int = 1):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, symbol, side, qty, type, limit_price, fee, tax,
                       (qty * limit_price) AS gross_total,
                       CASE
                           WHEN side='buy' THEN (qty * limit_price) + COALESCE(fee,0) + COALESCE(tax,0)
                           ELSE (qty * limit_price) - COALESCE(fee,0) - COALESCE(tax,0)
                       END AS net_total
                FROM orders WHERE status='pending' AND tenant_id=%s
                ORDER BY id DESC LIMIT %s
                """,
                (tenant_id, limit),
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception:
        return []
