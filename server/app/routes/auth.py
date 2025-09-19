from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas import auth as auth_schemas
from app.db.database import get_db
from app.services import auth_services
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(request_data: auth_schemas.LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = auth_services.authenticate_user(db, request_data.username, request_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    payload = auth_services.login_user(db, user)
    access_token = payload["access_token"]
    refresh_token = payload["refresh_token"]

    response.set_cookie(
        key=settings.ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )

    return {"status": "success", "message": "Black Channel's Drop"}
