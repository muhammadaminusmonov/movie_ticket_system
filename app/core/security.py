import os
import hashlib
import base64
from datetime import datetime, timedelta

import bcrypt
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def _prehash(password: str) -> bytes:
    """
    SHA-256 pre-hash before bcrypt.

    WHY: bcrypt truncates at 72 bytes. Any password longer than that gets the
    same hash as its first 72 bytes — a real security hole for long passwords.
    SHA-256 collapses any length to a fixed 44-char base64 string, safely
    within the limit. This is the same pattern Django's bcrypt hasher uses.
    """
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)  # always 44 ASCII bytes — well within 72


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_prehash(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(_prehash(plain), hashed.encode("utf-8"))


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Returns {"sub": user_id, "role": role} or raises JWTError."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])