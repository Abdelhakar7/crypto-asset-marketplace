from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document
from pydantic import Field, EmailStr
from pymongo import IndexModel

class User(Document):
    
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    email: EmailStr
    hashed_password: str
    #first_name: Optional[str] = None 
    profile_picture_url: Optional[str] = None  # <-- add this
    #last_name: Optional[str] = None
    disabled: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_admin: bool = False
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    
    @classmethod
    async def by_email(cls, email: str) -> "User":
        return await cls.find_one(cls.email == email)
    

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("username", 1)], unique=True),  # Use IndexModel
            IndexModel([("email", 1)], unique=True)      # Use IndexModel
        ]
