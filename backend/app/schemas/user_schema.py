from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    username: str
    #first_name: Optional[str] = None
    #last_name: Optional[str] = None
   # profile_picture: Optional[str] = None  # URL or path to profile picture


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    username: str
    #profile_picture: Optional[str] = None  # URL or path to profile picture
    disabled: Optional[bool] = None
    created_at: datetime

    class Config:
        orm_mode = True
        

class UserUpdate(BaseModel):
     username : Optional[str] = None
     password :  Optional[str] = None
     
