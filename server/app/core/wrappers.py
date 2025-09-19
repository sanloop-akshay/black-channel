from functools import wraps
from fastapi import Request, HTTPException, status
from app.core.security import is_token_blacklisted
from app.core.config import settings

def token_not_blacklisted(token_type: str = "access"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Request object missing"
                )
            token_name = settings.ACCESS_COOKIE_NAME if token_type == "access" else settings.REFRESH_COOKIE_NAME
            token = request.cookies.get(token_name)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"{token_type.capitalize()} token missing"
                )
            if is_token_blacklisted(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"{token_type.capitalize()} token is blacklisted"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
