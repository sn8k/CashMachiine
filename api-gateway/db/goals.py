"""Goals repository v0.1.1 (2025-08-20)"""
from psycopg2.extras import RealDictCursor
from . import get_connection


def fetch_goals(tenant_id: int):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, name, start_capital, target_amount, deadline FROM goals WHERE tenant_id=%s ORDER BY id",
                (tenant_id,),
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception:
        return []


def create_goal(goal: dict, tenant_id: int):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO goals (user_id, name, start_capital, target_amount, deadline, tenant_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, name, start_capital, target_amount, deadline
                """,
                (
                    goal.get("user_id"),
                    goal.get("name"),
                    goal.get("start_capital"),
                    goal.get("target_amount"),
                    goal.get("deadline"),
                    tenant_id,
                ),
            )
            conn.commit()
            return dict(cur.fetchone())
    except Exception:
        return {}


def fetch_goal_status(goal_id: int, tenant_id: int):
    try:
        with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    COALESCE(SUM(CASE WHEN status='done' THEN 1 END),0) AS done,
                    COALESCE(SUM(CASE WHEN status='pending' THEN 1 END),0) AS pending
                FROM actions a
                JOIN goals g ON g.id = a.goal_id
                WHERE a.goal_id=%s AND g.tenant_id=%s
                """,
                (goal_id, tenant_id),
            )
            row = cur.fetchone()
            return {"goal_id": goal_id, **row} if row else {"goal_id": goal_id, "done": 0, "pending": 0}
    except Exception:
        return {"goal_id": goal_id, "done": 0, "pending": 0}
