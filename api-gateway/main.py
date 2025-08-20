"""FastAPI app exposing goals, actions and analytics endpoints with JWT auth v0.3.3 (2025-08-20)"""
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
    UploadFile,
    File,
    Form,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from datetime import date
from pathlib import Path
import sys
import requests
import asyncio
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db.goals import fetch_goals, create_goal, fetch_goal_status
from db.actions import fetch_actions_today, check_action
from db.orders import fetch_orders_preview
from common.events import emit_event
from messaging import EventConsumer
from auth import router as auth_router

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
app.include_router(auth_router, prefix="/auth")
subscriptions: list[dict] = []
ws_clients: list[WebSocket] = []
event_queue: asyncio.Queue = asyncio.Queue()

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
    response.headers["X-API-Version"] = "v0.3.3"
    return response


async def dispatch_events():
    while True:
        message = await event_queue.get()
        alive: list[WebSocket] = []
        for ws in ws_clients:
            try:
                await ws.send_json(message)
                alive.append(ws)
            except Exception:
                pass
        ws_clients[:] = alive


@app.on_event("startup")
async def start_event_consumer() -> None:
    loop = asyncio.get_running_loop()
    try:
        consumer = EventConsumer(settings.rabbitmq_url, "api-gateway-ws")
    except Exception as exc:  # pragma: no cover - best effort
        logger.warning("event consumer disabled", extra={"error": str(exc)})
        return

    def handler(msg: dict) -> None:
        asyncio.run_coroutine_threadsafe(event_queue.put(msg), loop)

    threading.Thread(target=consumer.start, args=(handler,), daemon=True).start()
    asyncio.create_task(dispatch_events())


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    ws_clients.append(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        if ws in ws_clients:
            ws_clients.remove(ws)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), required_role: str | None = None):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    role = payload.get("role")
    tenant_id = payload.get("tenant_id")
    if tenant_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing tenant")
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

class AlertSubscription(BaseModel):
    user_id: int
    metric: str
    threshold: float
@app.get("/goals")
def get_goals(payload: dict = Depends(role_checker("user"))):
    return {"goals": fetch_goals(payload["tenant_id"])}

@app.post("/goals")
def post_goal(goal: GoalCreate, payload: dict = Depends(role_checker("admin"))):
    result = create_goal(goal.model_dump(), payload["tenant_id"])
    if result:
        emit_event("goal_created", {"goal_id": result["id"], "tenant_id": payload["tenant_id"]})
    return {"goal": result}


@app.get("/goals/{goal_id}/status")
def goal_status(goal_id: int, payload: dict = Depends(role_checker("user"))):
    return fetch_goal_status(goal_id, payload["tenant_id"])


@app.get("/actions")
def get_actions(_: dict = Depends(role_checker("admin"))):
    return {"actions": []}


@app.get("/actions/today")
def get_actions_today(payload: dict = Depends(role_checker("user"))):
    return {"actions": fetch_actions_today(payload["tenant_id"])}


@app.post("/actions/{action_id}/check")
def post_check_action(action_id: int, payload: dict = Depends(role_checker("admin"))):
    result = check_action(action_id, payload["tenant_id"])
    if not result:
        raise HTTPException(status_code=404, detail="Action not found")
    return result


@app.get("/orders/preview")
def get_orders_preview(limit: int = 10, payload: dict = Depends(role_checker("user"))):
    return {"orders": fetch_orders_preview(limit, payload["tenant_id"])}

@app.post("/alerts/subscribe")
def subscribe_alert(alert: AlertSubscription, payload: dict = Depends(role_checker("user"))):
    subscriptions.append({**alert.model_dump(), "tenant_id": payload["tenant_id"]})
    emit_event("alert_subscribed", alert.model_dump())
    return {"status": "subscribed"}


@app.post("/onboard")
async def onboard(
    user_id: int = Form(...),
    document: UploadFile = File(...),
    payload: dict = Depends(role_checker("user")),
):
    files = {"document": (document.filename, await document.read(), document.content_type)}
    try:
        resp = requests.post(
            f"{settings.kyc_service_url}/kyc/upload",
            data={"user_id": user_id},
            files=files,
            timeout=5,
        )
    except requests.RequestException as exc:
        logger.error("KYC upload failed", extra={"error": str(exc)})
        raise HTTPException(status_code=502, detail="KYC service unavailable")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="KYC upload failed")
    return resp.json()


@app.get("/kyc/status/{user_id}")
def kyc_status(user_id: int, payload: dict = Depends(role_checker("user"))):
    try:
        resp = requests.get(
            f"{settings.kyc_service_url}/kyc/status/{user_id}", timeout=5
        )
    except requests.RequestException as exc:
        logger.error("KYC status failed", extra={"error": str(exc)})
        raise HTTPException(status_code=502, detail="KYC service unavailable")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="KYC status error")
    return resp.json()


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
