from beanie import Document
from enum import Enum
from typing import ClassVar
from pydantic import Field , validator
from pymongo import IndexModel, ASCENDING

class CategoryEnum(str, Enum):
    ART = "art"
    MUSIC = "music"
    PHOTOGRAPHY = "photography"
    COLLECTIBLES = "collectibles"
    GAMING = "gaming"
    SPORTS = "sports"
    VIRTUAL_REAL_ESTATE = "virtual_real_estate"

class Category(Document):
    category_id: int 
    name: CategoryEnum
    @validator('category_id')
    def category_id_must_not_be_none(cls, v):
        if v is None:
            raise ValueError('category_id must not be None')
        return v
    
    class Settings:
        name = "categories"
        indexes = [
            IndexModel([("category_id", ASCENDING)], unique=True)  # Correct index syntax
        ]
    
    # Class variable to store predefined categories
    PREDEFINED_CATEGORIES: ClassVar[list] = [
        {"category_id": 1, "name": CategoryEnum.ART},
        {"category_id": 2, "name": CategoryEnum.MUSIC},
        {"category_id": 3, "name": CategoryEnum.PHOTOGRAPHY},
        {"category_id": 4, "name": CategoryEnum.COLLECTIBLES},
        {"category_id": 5, "name": CategoryEnum.GAMING},
        {"category_id": 6, "name": CategoryEnum.SPORTS},
        {"category_id": 7, "name": CategoryEnum.VIRTUAL_REAL_ESTATE},
    ]

