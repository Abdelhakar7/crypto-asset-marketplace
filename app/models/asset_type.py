from beanie import Document
from enum import Enum
from typing import ClassVar
from pydantic import Field
from pymongo import IndexModel, ASCENDING

class AssetTypeEnum(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    PDF = "pdf"

class AssetType(Document):
    asset_type_id: int 
    name: AssetTypeEnum
    mime_types: list[str]
    
    class Settings:
        name = "asset_types"
        indexes = [
            IndexModel([("asset_type_id", ASCENDING)], unique=True)  # Correct index syntax
        ]
    
    PREDEFINED_TYPES: ClassVar[list] = [
        {
            "asset_type_id": 1,  # Using id instead of type_id
            "name": AssetTypeEnum.IMAGE,
            "mime_types": ["image/jpeg", "image/png", "image/gif", "image/webp"]
        },
        {
            "asset_type_id": 2,
            "name": AssetTypeEnum.VIDEO,
            "mime_types": ["video/mp4", "video/webm", "video/quicktime"]
        },
        {
            "asset_type_id": 3,
            "name": AssetTypeEnum.PDF,
            "mime_types": ["application/pdf"]
        }
    ]