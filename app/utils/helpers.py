from tempfile import TemporaryFile
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import hashlib
from typing import Tuple
from app.core.config import settings
import os
from tempfile import NamedTemporaryFile
from pathlib import Path

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


async def verify_type(file_extention : str) -> str:

    video_extensions = ['mp4', 'mov', 'avi',]
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    pf_extensions = ['pdf']

    if file_extention in video_extensions:
        return 'video'
    if file_extention in image_extensions:
        return 'image'
    if file_extention in pf_extensions: 
        return 'pdf'
    return "error type not supported "    

async def stream_upload(file: UploadFile) -> Tuple[str, str ,str]:
    """
    Stream file upload to Cloudinary with memory-efficient approach
    Returns: (file_url, content_hash)
    """
    hasher = hashlib.sha256()
    
    # Use a smaller chunk size for faster processing
    chunk_size = 256 * 1024  # 256KB chunks
    
    # Use NamedTemporaryFile to get a file path Cloudinary can use directly
    with NamedTemporaryFile(delete=False) as temp_file:
        try:
            # Read and hash file in smaller chunks
            while chunk := await file.read(chunk_size):
                hasher.update(chunk)
                temp_file.write(chunk)
            
            # Close file to ensure all data is written
            temp_file.close()
            
            # Get content hash before upload starts
            content_hash = hasher.hexdigest()
            
            # Upload to cloudinary - use resource_type="auto" for better MIME type detection
            result = cloudinary.uploader.upload(
                temp_file.name,
                resource_type="auto", 
                use_filename=True
            )

            file_extension = get_file_extension(file.filename)
            asset_type = await verify_type(file_extension)
            if asset_type == "error type not supported":
                raise ValueError(f"Unsupported file type.{file_extension}")
            
            
            return result['secure_url'], content_hash ,asset_type
        finally:
            # Clean up temp file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)