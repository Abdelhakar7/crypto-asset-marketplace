from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.user_model import User
from app.models.asset_model import  Asset
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import dns.resolver
from app.api.router import api_router as router
from app.models.category_model import Category
from app.models.asset_type import AssetType
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure Google Public DNS
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']

    # Initialize MongoDB & Beanie
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[settings.DATABASE_NAME]
    await init_beanie(
        database=db_client,
        document_models=[User, Asset ,Category ,AssetType]  # Add more models as needed
    )
    
        # Initialize predefined categories
    for category_data in Category.PREDEFINED_CATEGORIES:
        logger.info(f"Processing category: {category_data}")
        try:
            # Explicitly ensure ID is set
            if 'category_id' not in category_data or category_data['category_id'] is None:
                logger.error(f"Invalid category data, missing ID: {category_data}")
                continue

            existing = await Category.find_one({"category_id": category_data["category_id"]})
            if not existing:
                # Create with explicit ID to ensure it's set
                category = Category(category_id=category_data["category_id"], name=category_data["name"])
                logger.info(f"Category object before insert: {category.dict()}")
                await category.insert()
                logger.info(f"Created category: {category_data['name']}")
        except Exception as e:
            logger.error(f"Error creating category {category_data}: {str(e)}")
            
        # Initialize predefined asset types
    for type_data in AssetType.PREDEFINED_TYPES:
        logger.info(f"Processing asset type: {type_data}")
        try:
            # Explicitly ensure ID is set
            if 'asset_type_id' not in type_data or type_data['asset_type_id'] is None:
                logger.error(f"Invalid asset type data, missing ID: {type_data}")
                continue
            
            existing = await AssetType.find_one({"asset_type_id": type_data["asset_type_id"]})
            if not existing:
                # Create with explicit ID to ensure it's set
                asset_type = AssetType(
                    asset_type_id=type_data["asset_type_id"],
                    name=type_data["name"],
                    mime_types=type_data["mime_types"]
                )
                logger.info(f"Asset type object before insert: {asset_type.dict()}")
                await asset_type.insert()
                logger.info(f"Created asset type: {type_data['name']}")
        except Exception as e:
            logger.error(f"Error creating asset type {type_data}: {str(e)}")

    logger.info("✅ Beanie initialized and connected to MongoDB.")
    yield  # App runs after this

# FastAPI instance with lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to NFT Digital Marketplace API. See /docs for API documentation."}
