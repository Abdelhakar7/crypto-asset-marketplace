from fastapi import APIRouter, Depends, HTTPException ,status
from pymongo.errors import DuplicateKeyError
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.services.user_service import UserService
from app.api.api_v1.auth.jwt import get_current_active_user
from app.models.user_model import User

user_router = APIRouter()


@user_router.post("/create", summary="Create a new user", response_model=UserOut)
async def creat_user(data : UserCreate):

       try:
               user = await UserService.create_user(data)
               return user
       except DuplicateKeyError as e:
        # Parse the error details
          error_message = str(e)
          if "email_1" in error_message:
              detail = "Email already registered"
          elif "username_1" in error_message:
            detail = "Username already taken"
          else:
            detail = "Duplicate entry detected"
            
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
          )
       except Exception as e:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
       
@user_router.get("/me", response_model=UserOut, summary="Get current user profile")
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile information.
    Requires authentication.
    """
    return current_user


@user_router.put("/update", response_model=UserOut, summary="Update user profile")
async def update_user(data: UserUpdate, current_user: User = Depends(get_current_active_user)):
 
    user = await UserService.update_user(current_user.user_id ,data)
    return user
