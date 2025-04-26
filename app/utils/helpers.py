import cloudinary
import cloudinary.uploader
from fastapi import UploadFile ,HTTPException
from typing import Tuple
from app.core.config import settings
from app.core.security import asset_hash
import asyncio
from io import BytesIO
from imagehash import hex_to_hash
from fastapi import HTTPException
from app.models.asset_model import Asset

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


def get_file_extension(file_name: str) -> str:
    """
    Splits on the last dot and returns what's after (lower-cased).
    If there's no dot, returns an empty string.
    """
    if "." not in file_name:
        return ""
    
    _, ext = file_name.rsplit(".", 1)
    return ext.lower()


def verify_type(file_extension: str) -> str:
    """Verify and return file type based on extension"""
    video_extensions = ['mp4', 'mov', 'avi']
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    pdf_extensions = ['pdf']

    extension = file_extension.lower()
    
    if extension in video_extensions:
        return 'video'
    if extension in image_extensions:
        return 'image'
    if extension in pdf_extensions:
        return 'pdf'
    
    raise HTTPException(
        status_code=400,
        detail=f"File type not supported: {extension}"
    )

async def stream_upload(file: UploadFile) -> Tuple[str, str, str, str]:
    """
    Stream file upload to Cloudinary with duplicate detection
    Returns: (file_url, content_hash, asset_type, public_id)
    """
    try:
        # Read content and determine type

        content = await file.read()
        extension = get_file_extension(file.filename)
        asset_type = verify_type(extension)  # Remove await since it's no longer async

        # Generate content hash
        content_hash = await asyncio.to_thread(asset_hash, content, asset_type)

        # Check for duplicates based on asset type
        if asset_type == "image":
            new_hash = hex_to_hash(content_hash)
            existing_assets = await Asset.find(
                {"asset_type": 1}
            ).to_list()
            
            for existing in existing_assets:
                old_hash = hex_to_hash(existing.content_hash)
                if abs(new_hash - old_hash) < 5:
                    raise HTTPException(
                        status_code=409,
                        detail="Similar image already exists"
                    )
        else:
            # For non-image files, check exact hash match
            existing = await Asset.find_one({"content_hash": content_hash})
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail="Identical content already exists"
                )

        # Map asset_type to Cloudinary resource_type
        resource_type = {
            "image": "image",
            "video": "video",
            "pdf": "raw"
        }.get(asset_type)

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            BytesIO(content),
            resource_type=resource_type,
            use_filename=True
        )

        return result["secure_url"], content_hash, asset_type

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )