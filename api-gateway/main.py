"""FastAPI app exposing goals and actions endpoints with JWT auth v0.2.1 (2025-08-19)"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os

from common.monitoring import setup_logging, setup_metrics, setup_tracer

SECRET_KEY = "secret"
ALGORITHM = "HS256"

security = HTTPBearer()

app = FastAPI()

logger = setup_logging("api-gateway", remote_url=os.environ.get("REMOTE_LOG_URL"))
REQUEST_COUNT = setup_metrics("api-gateway", port=int(os.environ.get("METRICS_PORT", "9001")))
tracer = setup_tracer("api-gateway")


@app.middleware("http")
async def add_version_header(request: Request, call_next):
    with tracer.start_as_current_span(request.url.path):
        response = await call_next(request)
    REQUEST_COUNT.inc()
    response.headers["X-API-Version"] = "v0.2.1"
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


@app.get("/goals")
def get_goals(_: dict = Depends(role_checker("user"))):
    return {"goals": []}


@app.get("/actions")
def get_actions(_: dict = Depends(role_checker("admin"))):
    return {"actions": []}
