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
        document_models=[User, Asset]  # Add more models as needed
    )

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
