from fastapi import UploadFile, HTTPException
from app.models.asset_model import Asset
from app.models.category_model import Category
from app.models.asset_type import AssetType
from app.schemas.asset_schema import AssetCreate ,AssetResponse
from app.utils.helpers import stream_upload 
from beanie import Link
from uuid import UUID
from app.models.user_model import User
from pymongo.errors import DuplicateKeyError

class AssetService:
    async def create_asset(
        self,
        asset_data: AssetCreate,
        file: UploadFile,
        user_id: UUID
    ) -> AssetResponse:
        try:
            # Upload file to cloudinary
            file_url, content_hash , asset_type = await stream_upload(file)

            asset_type_doc = await AssetType.find_one(AssetType.name == asset_type)



            # Get category documents
            categories = []
            for category_name in asset_data.categories:
                category = await Category.find_one({"name": category_name})
                if not category:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Category not found: {category_name}"
                    )
                categories.append(category)

            # Get user document
            user = await User.find_one({"user_id": user_id})
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )

            # Check if content hash already exists
            existing_asset = await Asset.find_one({"content_hash": content_hash})
            if existing_asset:
                raise HTTPException(
                    status_code=409,  # Conflict
                    detail="This content has already been uploaded. Duplicate content is not allowed."
                )

            # Create new asset
            new_asset = Asset(
                title=asset_data.title,
                description=asset_data.description,
                asset_type=asset_type_doc.asset_type_id,
                price=asset_data.price,
                file_url=file_url,
                content_hash=content_hash,
                owner_id=user,
                categories=categories,
                metadata=asset_data.metadata
            )

            await new_asset.insert()
            return AssetResponse.from_asset(new_asset)
            
        except DuplicateKeyError as e:
            error_message = str(e)
            if "content_hash" in error_message:
                raise HTTPException(
                    status_code=409,  # Conflict
                    detail="This content has already been uploaded. Duplicate content is not allowed."
                )
            elif "asset_id" in error_message:
                raise HTTPException(
                    status_code=409,
                    detail="Asset ID conflict. Please try again."
                )
            else:
                raise HTTPException(
                    status_code=409,
                    detail="Duplicate record detected."
                )
        except Exception as e:
            # Re-raise HTTP exceptions as is
            if isinstance(e, HTTPException):
                raise e
            
            # For other exceptions, provide a generic error
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while creating the asset: {str(e)}"
            )



