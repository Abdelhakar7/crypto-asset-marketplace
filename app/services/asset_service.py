from fastapi import UploadFile, HTTPException
from app.models.asset_model import Asset
from app.models.category_model import Category
from app.models.asset_type import AssetType
from app.schemas.asset_schema import AssetCreate ,AssetResponse , AssetUpdate
from datetime import datetime
from app.utils.helpers import stream_upload 
from uuid import UUID
from app.models.user_model import User

class AssetService:
    async def create_asset(
        self,
        asset_data: AssetCreate,
        file: UploadFile,
        user_id: UUID
    ) -> AssetResponse:
        try:
            # Upload file to cloudinary - exceptions already handled in helpers.py
            file_url, content_hash, asset_type = await stream_upload(file)

            # Get asset type document
            asset_type_doc = await AssetType.find_one(AssetType.name == asset_type)
            if not asset_type_doc:
                raise HTTPException(
                    status_code=404,
                    detail=f"Asset type not found: {asset_type}"
                )

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
                #get category ids
            category_ids = [category.category_id for category in categories]

            # Get user document
            user = await User.find_one({"user_id": user_id})
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )

            # Create new asset
            new_asset = Asset(
                title=asset_data.title,
                description=asset_data.description,
                asset_type=asset_type_doc.asset_type_id,
                price=asset_data.price,
                file_url=file_url,
                content_hash=content_hash,
                owner_id=user.user_id,
                category_ids=category_ids,
                metadata=asset_data.metadata
            )

            await new_asset.insert()
            return await AssetResponse.from_asset(new_asset)
            
        except HTTPException:
            # Re-raise HTTP exceptions as is
            raise
        except Exception as e:
            # For unexpected errors only
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error creating asset: {str(e)}"
            )
    async def get_all_assets(self) -> list[AssetResponse]:
        """Get all assets"""
        try:
            assets = await Asset.find_all().to_list()
            return [await AssetResponse.from_asset(asset) for asset in assets]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error fetching assets: {str(e)}"
            )
        
    async def get_user_assets(self, user_id: UUID) -> list[AssetResponse]:
        #hmmmmmmmmmm
        try:
            assets = await Asset.find(Asset.owner_id == user_id).to_list()
            return [await AssetResponse.from_asset(asset) for asset in assets]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error fetching user assets: {str(e)}"
            )
        
        # aya z3ma lokan njikngoulek salut rory i missed you wech ray7a diri ??
    async def get_asset(self, asset_id: UUID) -> AssetResponse:
        try:
            asset = await Asset.find_one(Asset.asset_id == asset_id)
            if not asset:
                raise HTTPException(
                    status_code=404,
                    detail="Asset not found"
                )
            return await AssetResponse.from_asset(asset)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error fetching asset: {str(e)}"

            )
        

        
    async def update_asset(self ,asset_id :UUID, data: AssetUpdate ,user_id : UUID) -> AssetResponse:
        try:
            asset = await Asset.find_one((Asset.asset_id == asset_id) and (Asset.owner_id ==user_id) )
            update_data = data.dict(exclude_unset=True)
            if not asset:
                raise HTTPException(
                    status_code=404,
                    detail="Asset not found"
                )
    # Handle categories if provided
            if "categories" in update_data:
                categories = []
                for category_name in update_data["categories"]:
                    category = await Category.find_one({"name": category_name})
                    if not category:
                       raise HTTPException(
                          status_code=404,
                          detail=f"Category not found: {category_name}"
                           )
                    categories.append(category)
                update_data["category_ids"] = [category.category_id for category in categories]
                del update_data["categories"]  # Remove categories from update_data
                # Update the asset in the database
            update_data["updated_at"] = datetime.now()
            result = await asset.update({"$set": update_data})
            return await AssetResponse.from_asset(result)
        except HTTPException:
            # Re-raise HTTP exceptions as is
            raise




