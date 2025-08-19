"""Orders repository v0.1.1 (2025-08-20)"""
from psycopg2.extras import RealDictCursor
from . import get_connection


def fetch_orders_preview(limit: int = 10, tenant_id: int = 1):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, symbol, side, qty, type, limit_price
                FROM orders WHERE status='pending' AND tenant_id=%s
                ORDER BY id DESC LIMIT %s
                """,
                (tenant_id, limit),
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception:
        return []
