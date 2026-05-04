from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_token
from app.domain.user import UserRole

bearer_scheme = HTTPBearer()


# ── Database ────────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Auth ─────────────────────────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Decode JWT and return {"user_id": str, "role": str}. Raises 401 if invalid."""
    try:
        payload = decode_token(credentials.credentials)
        return {"user_id": payload["sub"], "role": payload["role"]}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def require_owner(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] not in (UserRole.OWNER, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Cinema Owner access required")
    return current_user


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user