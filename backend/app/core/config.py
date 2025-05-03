from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from decouple import config


class Settings(BaseSettings):
    # General settings
    PROJECT_NAME: str = "NFT Digital Marketplace"
    API_V1_STR: str = "/api/v1"

    # MongoDB settings
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    DATABASE_NAME: str = config("DATABASE_NAME", default="nft_marketplace")

    # JWT settings
    SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    REFRESH_SECRET_KEY: str = config("JWT_SECRET_REFRESH_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # Optional

    # CORS
    ALLOWED_HOSTS: List[AnyHttpUrl] = []

    # Roles
    USER_ROLE: str = "user"
    ADMIN_ROLE: str = "admin"

    CLOUDINARY_CLOUD_NAME : str = config("CLOUDINARY_CLOUD_NAME" , cast =str)
    CLOUDINARY_API_KEY : int =config("CLOUDINARY_API_KEY" , cast =str)
    CLOUDINARY_API_SECRET :str = config("CLOUDINARY_API_SECRET" , cast =str)

    class Config:
        case_sensitive = True


settings = Settings()
