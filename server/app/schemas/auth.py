# app/schemas/auth.py
from pydantic import BaseModel, Field, constr
from typing import Optional
from uuid import UUID
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=1)

class UserOut(BaseModel):
    id: UUID
    username: str
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
