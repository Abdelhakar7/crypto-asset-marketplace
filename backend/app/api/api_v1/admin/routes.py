from fastapi import APIRouter ,Depends
from app.api.api_v1.auth.jwt import get_current_active_superuser
from app.models.user_model import User 
from app.services.user_service import UserService
from uuid import UUID
admin_router = APIRouter()

@admin_router.get("/admin", summary="Admin route")
async def admin_route(current_user:  User = Depends(get_current_active_superuser)):
    """
    Admin route that requires authentication.
    """
    return {"message": "Welcome to the admin route!", "user": current_user}


@admin_router.get("/users", summary="Get all users")
async def get_all_users(current_user: User = Depends(get_current_active_superuser)):
    """
    Get all users. Requires admin privileges.
    """
    # Assuming you have a method to get all users
    users = await UserService.get_all_users()
    return users
@admin_router.get("/users/{user_id}", summary="Get user by ID")
async def get_user_by_id(user_id: UUID, current_user: User = Depends(get_current_active_superuser)):
    """
    Get user by ID. Requires admin privileges.
    """
    # Assuming you have a method to get a user by ID
    user = await UserService.get_user_by_id(user_id)
    if not user:
        return {"message": "User not found"}
    return user
@admin_router.delete("/users/{user_id}", summary="Delete user by ID")
async def delete_user_by_id(user_id: UUID, current_user: User = Depends(get_current_active_superuser)):
    """
    Delete user by ID. Requires admin privileges.
    """
    # Assuming you have a method to delete a user by ID
    user = await UserService.get_user_by_id(user_id)
    if not user:
        return {"message": "User not found"}
    await user.delete()
    return {"message": "User deleted successfully"}

@admin_router.post("/users/{user_id}/activate", summary="Activate user by ID")
async def activate_user_by_id(user_id: UUID, current_user: User = Depends(get_current_active_superuser)):
    """
    Activate user by ID. Requires admin privileges.
    """
    # Assuming you have a method to activate a user by ID
    user = await UserService.get_user_by_id(user_id)
    if not user:
        return {"message": "User not found"}
    user.disabled = False
    await user.save()
    return {"message": "User activated successfully"}



@admin_router.post("/users/{user_id}/deactivate", summary="Deactivate user by ID")
async def deactivate_user_by_id(user_id: UUID, current_user: User = Depends(get_current_active_superuser)):
    """
    Deactivate user by ID. Requires admin privileges.
    """
    # Assuming you have a method to deactivate a user by ID
    user = await UserService.get_user_by_id(user_id)
    if not user:
        return {"message": "User not found"}
    user.disabled = True
    await user.save()
    return {"message": "User deactivated successfully"}