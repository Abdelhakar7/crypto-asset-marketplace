from beanie import Document
from typing import Optional, Dict, Any ,List
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime
from pymongo import IndexModel
from app.models.user_model import User
from beanie import Link
from app.models.category_model import Category
from app.models.asset_type import AssetType

class Asset(Document):
    asset_id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    asset_type: str
    file_url: str
    price: float
    owner_id: Link[User]
    categories: List[Link[Category]]  # Required category, no longer Optional
    content_hash: str
    metadata: Optional[Dict[str, Any]] = {}
    is_minted: bool = False
    token_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "assets"
        indexes = [
            IndexModel([("asset_id", 1)], unique=True),
            IndexModel([("content_hash", 1)], unique=True),
            IndexModel([("owner_id", 1)]),
            IndexModel([("asset_type", 1)]),
            IndexModel([("category", 1)])
        ]

