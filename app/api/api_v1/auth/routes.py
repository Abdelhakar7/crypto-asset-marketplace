from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt ,JWTError
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user_model import User
from app.schemas.auth_schema import Token, LoginRequest
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Login endpoint that returns access and refresh tokens.
    """
    user = await UserService.authenticate_user(
        email=form_data.username, 
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is disabled
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    # Create tokens
    access_token = create_access_token(str(user.user_id))
    refresh_token = create_refresh_token(str(user.user_id))
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str) -> Any:
    """
    Refresh access token using a valid refresh token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )
    
    try:
        # Decode the refresh token
        payload = jwt.decode(
            refresh_token, 
            settings.REFRESH_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Parse token payload
        user_id = payload.get("sub")
        exp = payload.get("exp")
        
        # Check if token is expired
        if datetime.now().timestamp() > exp:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Find user by ID
    user = await User.find_one(User.user_id == UUID(user_id))
    if user is None or user.disabled:
        raise credentials_exception
    
    # Create new tokens
    access_token_expires = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.now() + timedelta(days=7)
    
    access_token = jwt.encode(
        {"sub": str(user.user_id), "exp": int(access_token_expires.timestamp())},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    new_refresh_token = jwt.encode(
        {"sub": str(user.user_id), "exp": int(refresh_token_expires.timestamp())},
        settings.REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
