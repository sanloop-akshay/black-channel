from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.schemas import auth as auth_schemas
from app.db.database import get_db
from app.services import auth_services
from app.core.config import settings
from app.core.logger import get_logger
from app.core import constants
from app.core.security import blacklist_token
router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger(__name__)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request_data: auth_schemas.LoginRequest, response: Response, db: Session = Depends(get_db)):
    logger.info(constants.AUTH_LOGIN_ATTEMPT.format(username=request_data.username))

    user = auth_services.authenticate_user(db, request_data.username, request_data.password)
    if not user:
        logger.warning(constants.AUTH_LOGIN_FAILED.format(username=request_data.username))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

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

    logger.info(constants.AUTH_LOGIN_SUCCESS.format(username=request_data.username))
    return {
        "status": status.HTTP_200_OK,
        "message": "Black Channel's Drop"
    }


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if not refresh_token:
        logger.warning(constants.AUTH_REFRESH_FAILED.format(username="Unknown"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token"
        )

    payload = auth_services.refresh_access_token(db, refresh_token)
    if not payload:
        logger.warning(constants.AUTH_REFRESH_FAILED.format(username="Unknown"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    new_access_token = payload["access_token"]
    username = payload["user"].username

    response.set_cookie(
        key=settings.ACCESS_COOKIE_NAME,
        value=new_access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    logger.info(constants.AUTH_REFRESH_SUCCESS.format(username=username))
    return {
        "status": status.HTTP_200_OK,
        "message": "Access token refreshed successfully"
    }

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response):
    access_token = request.cookies.get(settings.ACCESS_COOKIE_NAME)
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)

    if access_token:
        blacklist_token(access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        response.delete_cookie(settings.ACCESS_COOKIE_NAME)
        logger.info(constants.AUTH_ACCESS_TOKEN_BLACKLIST)

    if refresh_token:
        blacklist_token(refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        response.delete_cookie(settings.REFRESH_COOKIE_NAME)
        logger.info(constants.AUTH_ACCESS_TOKEN_BLACKLIST)

    return {
        "status": status.HTTP_200_OK,
        "message": "Successfully logged out"
    }