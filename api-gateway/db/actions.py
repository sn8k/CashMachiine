"""Actions repository v0.1.1 (2025-08-20)"""
from psycopg2.extras import RealDictCursor
from . import get_connection
from datetime import date


def fetch_actions_today(tenant_id: int):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT a.id, a.goal_id, a.day, a.title, a.status
                FROM actions a
                JOIN goals g ON g.id=a.goal_id
                WHERE a.day=%s AND g.tenant_id=%s
                ORDER BY a.id
                """,
                (date.today(), tenant_id),
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception:
        return []


def check_action(action_id: int, tenant_id: int):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE actions SET status='done'
                WHERE id=%s AND goal_id IN (SELECT id FROM goals WHERE tenant_id=%s)
                RETURNING id, status
                """,
                (action_id, tenant_id),
            )
            conn.commit()
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception:
        return {}
