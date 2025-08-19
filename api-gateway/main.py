"""FastAPI app exposing goals, actions and analytics endpoints with JWT auth v0.2.6 (2025-08-19)"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db.goals import fetch_goals, create_goal, fetch_goal_status
from db.actions import fetch_actions_today, check_action
from db.orders import fetch_orders_preview

from common.monitoring import (
    setup_logging,
    setup_metrics,
    setup_performance_metrics,
    setup_tracer,
)
from config import settings
from infra.cache import get_redis_client

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

security = HTTPBearer()

app = FastAPI()

logger = setup_logging("api-gateway", remote_url=settings.remote_log_url)
REQUEST_COUNT = setup_metrics("api-gateway", port=settings.api_gateway_metrics_port)
REQUEST_LATENCY = setup_performance_metrics("api-gateway")
tracer = setup_tracer("api-gateway")
redis_client = get_redis_client()
RATE_LIMIT = settings.rate_limit_per_minute


@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    key = f"rl:{client_ip}"
    current = redis_client.get(key)
    if current and int(current) >= RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})
    pipe = redis_client.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, 60)
    pipe.execute()
    return await call_next(request)


@app.middleware("http")
async def measure_latency(request: Request, call_next):
    with REQUEST_LATENCY.time():
        response = await call_next(request)
    return response


@app.middleware("http")
async def add_version_header(request: Request, call_next):
    with tracer.start_as_current_span(request.url.path):
        response = await call_next(request)
    REQUEST_COUNT.inc()
    response.headers["X-API-Version"] = "v0.2.6"
    return response


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), required_role: str | None = None):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    role = payload.get("role")
    if required_role and role != required_role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
    return payload


def role_checker(role: str):
    def checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
        return verify_token(credentials, role)
    return checker


class GoalCreate(BaseModel):
    user_id: int
    name: str
    start_capital: float | None = None
    target_amount: float | None = None
    deadline: date | None = None


@app.get("/goals")
def get_goals(_: dict = Depends(role_checker("user"))):
    return {"goals": fetch_goals()}


@app.post("/goals")
def post_goal(goal: GoalCreate, _: dict = Depends(role_checker("admin"))):
    return {"goal": create_goal(goal.dict())}


@app.get("/goals/{goal_id}/status")
def goal_status(goal_id: int, _: dict = Depends(role_checker("user"))):
    return fetch_goal_status(goal_id)


@app.get("/actions")
def get_actions(_: dict = Depends(role_checker("admin"))):
    return {"actions": []}


@app.get("/actions/today")
def get_actions_today(_: dict = Depends(role_checker("user"))):
    return {"actions": fetch_actions_today()}


@app.post("/actions/{action_id}/check")
def post_check_action(action_id: int, _: dict = Depends(role_checker("admin"))):
    result = check_action(action_id)
    if not result:
        raise HTTPException(status_code=404, detail="Action not found")
    return result


@app.get("/orders/preview")
def get_orders_preview(limit: int = 10, _: dict = Depends(role_checker("user"))):
    return {"orders": fetch_orders_preview(limit)}


@app.get("/analytics")
def get_analytics(_: dict = Depends(role_checker("admin"))):
    db_metrics: list[dict] = []
    try:
        with psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_pass,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT date, requests, errors FROM metrics_daily ORDER BY date DESC LIMIT 7"
                )
                db_metrics = [dict(row) for row in cur.fetchall()]
    except Exception:
        db_metrics = []
    observability = {"requests": REQUEST_COUNT._value.get()}
    return {"db_metrics": db_metrics, "observability": observability}
