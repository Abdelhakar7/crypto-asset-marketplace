from fastapi import APIRouter
from app.api.api_v1.users.routes import user_router
from app.api.api_v1.auth.routes import router as auth_router
from app.api.api_v1.asset.routes import asset_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(asset_router, prefix ="/assets" , tags=["asset"])


