from beanie import Document
from enum import Enum
from typing import ClassVar
from pydantic import Field
from pymongo import IndexModel, ASCENDING


class AssetType(Document):
    asset_type_id: int = Field(..., unique=True)
    name: str
    
    class Settings:
        name = "asset_types"
    