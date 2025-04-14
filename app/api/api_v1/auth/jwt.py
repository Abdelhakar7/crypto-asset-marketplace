from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID
from pydantic import ValidationError

from app.core.config import settings
from app.models.user_model import User
from app.schemas.auth_schema import TokenPayload
from app.services.user_service import UserService

# OAuth2 scheme for token extraction from request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    """
    print(f"DEBUG: Token received: {token[:10]}...")
    
    try:
        print("DEBUG: Attempting to decode token...")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"DEBUG: Token decoded successfully: {payload}")

        try:
            token_data = TokenPayload(**payload)
            print(f"DEBUG: TokenPayload created: {token_data}")
            
            now = datetime.now()
            exp_time = datetime.fromtimestamp(token_data.exp)
            print(f"DEBUG: Current time: {now}, Token expires: {exp_time}")
            
            if exp_time < now:
                print("DEBUG: Token has expired")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValidationError as ve:
            print(f"DEBUG: Pydantic validation error: {ve}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token payload structure",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except jwt.JWTError as je:
        print(f"DEBUG: JWT error: {je}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: Looking for user with ID: {token_data.sub}")
    try:
        user = await UserService.get_user_by_id(token_data.sub)
        print(f"DEBUG: User lookup result: {user}")
    except Exception as e:
        print(f"DEBUG: Error during user lookup: {e}")
        user = None
        
    if not user:
        print("DEBUG: User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: Authentication successful for user: {user.email}")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Dependency to get current active user (not disabled).
    """
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
