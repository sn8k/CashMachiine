"""FastAPI app exposing goals and actions endpoints with JWT auth v0.2.0"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

security = HTTPBearer()

app = FastAPI()


@app.middleware("http")
async def add_version_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-API-Version"] = "v0.2.0"
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
