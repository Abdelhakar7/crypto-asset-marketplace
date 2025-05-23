from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TokenPayload(BaseModel):
    sub: UUID  # User ID
    exp: int   # Expiration timestamp
   # is_admin = bool

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str
