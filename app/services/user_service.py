from app.schemas.user_schema import UserCreate
from app.models.user_model import User
from app.core.security import get_password_hash, verify_password
from typing import Optional

class UserService:
    @staticmethod
    async def create_user(user :UserCreate):
       user_in = User(
            email=user.email,
            username=user.username,
            hashed_password= get_password_hash(user.password)

       )      
       
       await user_in.insert()
       return user_in

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        user = await User.by_email(email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        return user

    @staticmethod
    async def get_user_by_id(user_id):
        return await User.find_one(User.user_id == user_id)
