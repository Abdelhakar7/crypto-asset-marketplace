from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
from PIL import Image 
from io import BytesIO
import imagehash
import hashlib
from app.utils.utils import normalized_text

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hashes the password using a secure hashing algorithm.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hash.
    """
    return password_context.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    expires = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": int(expires.timestamp())}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



def create_refresh_token(subject: str) -> str:
    expires = datetime.now() + timedelta(days=7)  # 7 days
    to_encode = {"sub": subject, "exp": int(expires.timestamp())}
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)



def  asset_hash( content : bytes , file_type : str) -> str:
     
     #  rbi wkilek ya roa 
     
     if file_type == "image" :
            # Open the image file
        with Image.open(BytesIO(content)) as img:
                # Calculate the perceptual hash
                hash_value = imagehash.phash(img)
                return str(hash_value)
        
     elif file_type == "pdf":
              text=normalized_text(content)
              return hashlib.sha256(text.encode("utf-8")).hexdigest()
     else:
                raise ValueError("Unsupported file type for hashing")
     

     # hiaba hadi conquered our instgram fyp
     
          
        
      
      
         
