"""OAuth2/OIDC and TOTP authentication utilities v0.1.0 (2025-08-20)"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import requests
import pyotp
import secrets
from common.monitoring import setup_logging
from config import settings

router = APIRouter()
logger = setup_logging("auth", remote_url=settings.remote_log_url)

TOTP_STORE: dict[int, dict[str, list[str] | str]] = {}


class UserId(BaseModel):
    user_id: int


class VerifyCode(UserId):
    code: str


class RecoverCode(UserId):
    backup_code: str


@router.get("/oauth/{provider}/login")
def oauth_login(provider: str, request: Request):
    if provider not in ("google", "github"):
        raise HTTPException(400, "Unsupported provider")
    redirect_uri = str(request.url_for("oauth_callback", provider=provider))
    if provider == "google":
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.google_client_id}&response_type=code&"
            f"redirect_uri={redirect_uri}&scope=openid%20email"
        )
    else:
        auth_url = (
            "https://github.com/login/oauth/authorize?"
            f"client_id={settings.github_client_id}&redirect_uri={redirect_uri}&scope=read:user"
        )
    logger.info("oauth_login", extra={"provider": provider})
    return {"auth_url": auth_url}


@router.get("/oauth/{provider}/callback", name="oauth_callback")
def oauth_callback(provider: str, code: str):
    if provider == "google":
        token_url = "https://oauth2.googleapis.com/token"
        client_id = settings.google_client_id
        client_secret = settings.google_client_secret
    elif provider == "github":
        token_url = "https://github.com/login/oauth/access_token"
        client_id = settings.github_client_id
        client_secret = settings.github_client_secret
    else:
        raise HTTPException(400, "Unsupported provider")
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "postmessage",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {"Accept": "application/json"}
    resp = requests.post(token_url, data=data, headers=headers, timeout=5)
    logger.info("oauth_callback", extra={"provider": provider, "status": resp.status_code})
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, "Token exchange failed")
    return resp.json()


@router.post("/2fa/setup")
def setup_2fa(payload: UserId):
    secret = pyotp.random_base32()
    codes = [secrets.token_hex(4) for _ in range(5)]
    TOTP_STORE[payload.user_id] = {"secret": secret, "codes": codes}
    logger.info("2fa_setup", extra={"user_id": payload.user_id})
    return {"secret": secret, "backup_codes": codes}


@router.post("/2fa/verify")
def verify_2fa(payload: VerifyCode):
    record = TOTP_STORE.get(payload.user_id)
    if not record:
        raise HTTPException(404, "2FA not configured")
    totp = pyotp.TOTP(record["secret"])
    if not totp.verify(payload.code):
        logger.warning("2fa_verify_failed", extra={"user_id": payload.user_id})
        raise HTTPException(401, "Invalid code")
    logger.info("2fa_verify", extra={"user_id": payload.user_id})
    return {"status": "verified"}


@router.post("/2fa/recover")
def recover_2fa(payload: RecoverCode):
    record = TOTP_STORE.get(payload.user_id)
    if not record:
        raise HTTPException(404, "2FA not configured")
    codes: list[str] = record["codes"]  # type: ignore[assignment]
    if payload.backup_code not in codes:
        logger.warning("2fa_recover_failed", extra={"user_id": payload.user_id})
        raise HTTPException(401, "Invalid backup code")
    codes.remove(payload.backup_code)
    logger.info("2fa_recover", extra={"user_id": payload.user_id})
    return {"status": "recovered"}
