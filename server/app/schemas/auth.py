# app/schemas/auth.py
from pydantic import BaseModel, Field, constr
from typing import Optional
from uuid import UUID
from datetime import datetime


class LoginRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=1)


