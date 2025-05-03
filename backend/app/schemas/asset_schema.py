from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.models.category_model import CategoryEnum
from decimal import Decimal
from uuid import UUID
from datetime import datetime
from app.models.asset_model import Asset
from fastapi import HTTPException
from app.models.category_model import Category

class AssetBase(BaseModel):
    """Schema for creating an asset"""
    title: str
    description: Optional[str] = None
    price: float
    categories: List[CategoryEnum]
    metadata: Optional[Dict[str, Any]] = {}

class AssetCreate (AssetBase):
    pass

class AssetResponse(AssetBase):
    """Schema for returning asset data"""
    asset_id: UUID
    file_url: str
    owner_id: UUID  # Change from UUID to str
    categories: List[str]  # Change from CategoryEnum to str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        
    @classmethod
    async def from_asset(cls, asset: Asset):
        
        #get category names from category ids
        category_names = []
        for category_id in asset.category_ids:
            category = await Category.find_one({"category_id": category_id})
            if category:
                category_names.append(category.name)
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Category not found: {category_id}"
                )
        """Convert Asset document to response schema"""
        
        

        # Add debugging to check asset fields
        print(f"Asset fields: {asset.dict()}")
        
        return cls(
            asset_id=asset.asset_id,
            title=asset.title,
            description=asset.description, # Asset type is already a string
            price=asset.price,
            categories=category_names,  # Changed from categories to category
            file_url=asset.file_url,  # Ensure this is correctly passed
            owner_id=asset.owner_id, 
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            metadata=asset.metadata
        )
    

class AssetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: Optional[List[CategoryEnum]] = None
    metadata: Optional[Dict[str, Any]] = None
