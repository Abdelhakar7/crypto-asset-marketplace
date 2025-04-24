from tempfile import TemporaryFile
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import hashlib
from typing import Tuple
from app.core.config import settings
import os
from tempfile import NamedTemporaryFile

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


async def stream_upload(file: UploadFile) -> Tuple[str, str]:
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
            
            return result['secure_url'], content_hash
        finally:
            # Clean up temp file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)