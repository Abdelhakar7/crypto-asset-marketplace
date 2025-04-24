from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from app.services.asset_service import AssetService
from app.schemas.asset_schema import AssetCreate, AssetResponse
from app.api.api_v1.auth.jwt import get_current_active_user
from app.models.user_model import User
from app.models.category_model import CategoryEnum
from decimal import Decimal
import json
from typing import Optional

asset_router = APIRouter()

@asset_router.post("/", response_model=AssetResponse)
async def create_asset(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    asset_type: str = Form(...),
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
        asset_type=asset_type,
        price=Decimal(str(price)),
        categories=categories_enum,
        metadata=metadata_dict
    )

    result = await asset_service.create_asset(
        asset_data=asset_data,
        file=file,
        user_id=current_user.user_id
    )
    return result