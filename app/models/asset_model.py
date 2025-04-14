from beanie import Document
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import Field
from datetime import datetime
from pymongo import IndexModel


class Asset(Document):
    asset_id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    asset_type: str  # e.g., "image", "video", "audio", "pdf"
    file_url: str  # URL or path to the uploaded file (in cloud or local)
    price: float
    owner_id: UUID  # UUID of the user who uploaded the asset

    content_hash: str  # hash of file content for uniqueness / security
    metadata: Optional[Dict[str, Any]] = {}  # can store resolution, format, etc.
    is_minted: bool = False
    token_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "assets"
        indexes = [
            IndexModel([("asset_id", 1)], unique=True),
            IndexModel([("content_hash", 1)], unique=True),
            IndexModel([("owner_id", 1)]),
            IndexModel([("asset_type", 1)]),
        ]

    class Config:
        schema_extra = {
            "example": {
                "asset_id": "6c6e1fc2-cc3e-4c8a-91c3-1fbc5fcbdcb1",
                "title": "Epic Music Track",
                "description": "High quality audio for games",
                "asset_type": "audio",
                "file_url": "https://example.com/files/audio123.mp3",
                "price": 12.99,
                "owner_id": "ec5a6a80-d5b0-4de9-a1e2-0ed6a74f0b77",
                "content_hash": "f9a8d8a...f3c0",
                "metadata": {"duration": "2:34", "format": "mp3"},
                "is_minted": False,
                "token_id": None,
                "created_at": "2025-04-12T14:30:00",
                "updated_at": None
            }
        }

