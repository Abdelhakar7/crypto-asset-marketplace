from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.models.category_model import CategoryEnum
from decimal import Decimal
from uuid import UUID
from datetime import datetime
from app.models.asset_model import Asset

class AssetBase(BaseModel):
    """Schema for creating an asset"""
    title: str
    description: Optional[str] = None
    asset_type: str
    price: Decimal
    categories: List[CategoryEnum]
    metadata: Optional[Dict[str, Any]] = {}

class AssetCreate (AssetBase):
    pass

class AssetResponse(AssetBase):
    """Schema for returning asset data"""
    asset_id: UUID
    file_url: str
    content_hash: str
    owner_id: str  # Change from UUID to str
    categories: List[str]  # Change from CategoryEnum to str
    is_minted: bool
    token_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        
    @classmethod
    def from_asset(cls, asset: Asset):
        """Convert Asset document to response schema"""
        # Add debugging to check asset fields
        print(f"Asset fields: {asset.dict()}")
        
        return cls(
            asset_id=asset.asset_id,
            title=asset.title,
            description=asset.description,
            asset_type=asset.asset_type,  # Asset type is already a string
            price=asset.price,
            categories=[cat.name.value for cat in asset.categories],  # Changed from categories to category
            file_url=asset.file_url,
            content_hash=asset.content_hash,  # Ensure this is correctly passed
            owner_id=str(asset.owner_id.user_id),  # Convert UUID to string
            is_minted=asset.is_minted,
            token_id=asset.token_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            metadata=asset.metadata
        )
    
