"""Actions repository v0.1.0 (2025-08-19)"""
from psycopg2.extras import RealDictCursor
from . import get_connection
from datetime import date


def fetch_actions_today():
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, goal_id, day, title, status FROM actions WHERE day=%s ORDER BY id",
                (date.today(),),
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception:
        return []


def check_action(action_id: int):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "UPDATE actions SET status='done' WHERE id=%s RETURNING id, status",
                (action_id,),
            )
            conn.commit()
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception:
        return {}
