from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException ,Path
from app.services.asset_service import AssetService
from app.schemas.asset_schema import AssetCreate, AssetResponse , AssetUpdate
from app.api.api_v1.auth.jwt import get_current_active_user
from app.models.user_model import User
from app.models.category_model import CategoryEnum
from decimal import Decimal
import json
from typing import Optional ,List
from uuid import UUID
asset_router = APIRouter()

@asset_router.post("/", response_model=AssetResponse)
async def create_asset(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    category: str = Form(...),  # Expect JSON array of category names
    metadata: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    asset_service: AssetService = Depends()
):
    """Create a new asset with file upload"""
    # Parse metadata if provided
    try:
        # Parse categories JSON array
        categories_list = json.loads(category)
        if not isinstance(categories_list, list):
            raise ValueError("Categories must be a list")
        
        # Validate each category
        categories_enum = [CategoryEnum(cat) for cat in categories_list]

        metadata_dict = json.loads(metadata) if metadata else {}
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Invalid metadata JSON format"
        )

    # Create AssetCreate instance
    asset_data = AssetCreate(
        title=title,
        description=description,
        price=price,
        categories=categories_enum,
        metadata=metadata_dict
    )

    result = await asset_service.create_asset(
        asset_data=asset_data,
        file=file,
        user_id=current_user.user_id
    )
    return result

@asset_router.get("/getall" , response_model=List[AssetResponse])
async def get_all_assets(
    current_user: User = Depends(get_current_active_user),
    asset_service: AssetService = Depends()
):
    """Get all assets"""
    result = await asset_service.get_all_assets()
    return result
@asset_router.get("/{user_id}", response_model=List[AssetResponse])
async def get_user_assets(
    user: User = Depends(get_current_active_user),
    asset_service: AssetService = Depends()
):
    """Get assets for a specific user"""
    result = await asset_service.get_user_assets(user_id=user.user_id)
    return result
@asset_router.get("/get/{asset_id}", response_model=AssetResponse)

async def get_asset(
    asset_id: UUID = Path(..., description="The ID of the asset to retrieve"),
    current_user: User = Depends(get_current_active_user),
    asset_service: AssetService = Depends()
):
    """Get a specific asset by ID"""
    result = await asset_service.get_asset(asset_id=asset_id)
    if not result:
        raise HTTPException(status_code=404, detail="Asset not found")
    return result

# imagine HIBA hhhhh hiba 
@asset_router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(data: AssetUpdate ,asset_id: UUID = Path(..., description="The ID of the asset to update"),
    current_user: User = Depends(get_current_active_user),
    asset_service: AssetService = Depends()
):
    """Update an existing asset"""
    result = await asset_service.update_asset(
        asset_id=asset_id,
        data=data,
        user_id=current_user.user_id
    )
    if not result:
        raise HTTPException(status_code=404, detail="Asset not found")
    return result

## saha rani zedt delete asset 

@asset_router.delete("/{asset_id}" ,summary= "Delete an asset")
async def delete_asset(
    asset_id: UUID = Path(..., description="The ID of the asset to delete"),
    current_user: User = Depends(get_current_active_user),
    asset_service: AssetService = Depends()
):
    """Delete an asset"""
    result = await asset_service.delete_asset(asset_id=asset_id , user_id=current_user.user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted successfully"}
    