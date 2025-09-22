from sqlalchemy.orm import Session
from app.db import models
from app.core import security
from app.core.config import settings
from datetime import datetime
from jose import JWTError
from app.core.logger import get_logger
from app.core import constants
from app.core.security import blacklist_token
import random
from app.core.settings import redis_client
from app.tasks.mailer_task import send_otp_email
from datetime import timedelta
import json
from app.db.models import User

logger = get_logger(__name__)
def generate_otp(length: int = 6) -> str:

    if length <= 0:
        raise ValueError("OTP length must be greater than 0")
    range_start = 10**(length - 1)
    range_end = (10**length) - 1
    return str(random.randint(range_start, range_end))


def authenticate_user(db: Session, username: str, password: str):

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None

    if not security.verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, user):
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = security.create_access_token(str(user.id), extra={"username": user.username})
    refresh_token = security.create_refresh_token(str(user.id))

    return {"access_token": access_token, "refresh_token": refresh_token, "user": user}


def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = security.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            return None
        user_id = payload.get("sub")
    except JWTError as e:
        return None

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    new_access_token = security.create_access_token(str(user.id), extra={"username": user.username})
    return {"access_token": new_access_token, "user": user}


def logout_user(access_token: str = None, refresh_token: str = None):

    if access_token:
        try:
            payload = security.decode_token(access_token)
            if payload.get("type") == "access":
                blacklist_token(access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
                logger.info(constants.AUTH_ACCESS_TOKEN_BLACKLIST)
        except JWTError:
            logger.warning(constants.AUTH_INVALID_ACCESS_TOKEN_BLACKLIST)

    if refresh_token:
        try:
            payload = security.decode_token(refresh_token)
            if payload.get("type") == "refresh":
                blacklist_token(refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
                logger.info(constants.AUTH_REFRESH_TOKEN_BLACKLIST)
        except JWTError:
            logger.warning(constants.AUTH_INVALID_REFRESH_TOKEN_BLACKLIST)



def signup_user(db, username: str, password: str, email: str):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return None  

    hashed_password = security.hash_password(password)
    otp = generate_otp()
    
    temp_user_data = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password
    }
    redis_client.setex(
        f"signup:{email}",
        timedelta(minutes=5),  
        json.dumps(temp_user_data) 
    )
    redis_client.setex(f"otp:{username}", timedelta(minutes=5), otp)
    send_otp_email.delay(email, otp)
    return {"status": "pending_verification", "message": "OTP sent to your email"}


def verify_otp_and_create_user(db, email: str, otp: str):

    stored_otp = redis_client.get(f"otp:{email}")
    if not stored_otp:
        return None, "OTP expired or invalid"

    if otp != stored_otp:
        return None, "Incorrect OTP"

    temp_user_json = redis_client.get(f"signup:{email}")
    if not temp_user_json:
        return None, "Kindly Signup First"

    temp_user_data = json.loads(temp_user_json)

    new_user = User(
        username=temp_user_data["username"],
        email=temp_user_data["email"],
        hashed_password=temp_user_data["hashed_password"]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    redis_client.delete(f"signup:{email}")
    redis_client.delete(f"otp:{email}")

    return new_user, None


def resend_otp(email: str):

    temp_user_json = redis_client.get(f"signup:{email}")
    if not temp_user_json:
        return None, "No pending signup found for this email"

    otp = generate_otp()

    redis_client.setex(f"otp:{email}", timedelta(minutes=5), otp)

    send_otp_email.delay(email, otp)

    return {"status": "pending_verification", "message": "OTP resent successfully"}, None
