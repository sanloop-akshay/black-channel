# app/schemas/auth.py
from pydantic import BaseModel, constr


class LoginRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=1)


