from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from app.core.settings import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(subject: str, expires_delta_minutes: int, token_type: str = "access", extra: Optional[Dict[str, Any]] = None) -> str:
    now = datetime.utcnow()
    exp = now + timedelta(minutes=expires_delta_minutes)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def create_access_token(subject: str, extra: Optional[Dict[str, Any]] = None) -> str:
    return create_token(subject, settings.ACCESS_TOKEN_EXPIRE_MINUTES, token_type="access", extra=extra)

def create_refresh_token(subject: str, extra: Optional[Dict[str, Any]] = None) -> str:
    return create_token(subject, settings.REFRESH_TOKEN_EXPIRE_MINUTES, token_type="refresh", extra=extra)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

def blacklist_token(token: str, expire_seconds: int):
    redis_client.set(token, "blacklisted", ex=expire_seconds)

def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(token) > 0
