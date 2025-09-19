from sqlalchemy.orm import Session
from app.db import models
from app.core import security
from app.core.config import settings
from datetime import datetime

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
