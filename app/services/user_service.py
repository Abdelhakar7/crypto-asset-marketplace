from app.schemas.user_schema import UserCreate, UserUpdate
from app.models.user_model import User
from app.core.security import get_password_hash, verify_password
from typing import Optional
from fastapi import HTTPException

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
    
    @staticmethod
    async def update_user(user_id, data: UserUpdate):
        user = await User.find_one(User.user_id == user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user fields
        user.username = data.username
        user.hashed_password = get_password_hash(data.password)
        
        # Save changes
        await user.save()
        
        # Refresh user from database to get updated values
        return await User.find_one(User.user_id == user_id)
        