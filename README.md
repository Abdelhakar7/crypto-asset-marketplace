# NFT-Based Digital Marketplace Backend

A FastAPI backend for a digital content marketplace where digital assets are represented as NFTs.

## Project Overview

This is a proof-of-concept API for a digital marketplace with NFT integration. The backend supports:

- User authentication (register, login, token management)
- User profile management
- Admin user management
- Future NFT asset management (endpoints prepared for implementation)

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PyMongo** - MongoDB driver for Python
- **JWT Authentication** - Token-based authentication
- **MongoDB** - NoSQL database for storing user and asset data

## Project Structure

```
.
├── app
│   ├── api
│   │   ├── api_v1
│   │   │   ├── auth           # Authentication endpoints
│   │   │   ├── users          # User endpoints
│   │   │   ├── admin          # Admin endpoints
│   │   ├── router.py          # API router aggregation
│   ├── core
│   │   ├── config.py          # Application configuration
│   │   ├── security.py        # Security utilities
│   ├── models                 # MongoDB models
│   ├── schemas                # Pydantic schemas for API
│   ├── services               # Business logic services
│   ├── utils                  # Utility functions
│   ├── app.py                 # FastAPI application
├── requirements.txt           # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB (local or hosted)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables (or they will use defaults):
   ```
   export MONGO_CONNECTION_STRING="your_mongodb_connection_string"
   export DATABASE_NAME="nft_marketplace"
   export SECRET_KEY="your_secret_key"
   ```

### Running the Application

```
uvicorn app.app:app --reload
```

The API will be available at http://localhost:8000

API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/logout` - Logout (client-side token removal)
- `POST /api/v1/auth/refresh` - Refresh token (placeholder)

### Users

- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Admin

- `GET /api/v1/admin/users` - List all users (admin only)
- `GET /api/v1/admin/users/{user_id}` - Get user details (admin only)
- `PUT /api/v1/admin/users/{user_id}` - Update user (admin only)
- `DELETE /api/v1/admin/users/{user_id}` - Delete user (admin only)

### Future NFT Asset Endpoints

The following endpoints are prepared for future implementation:

- `GET /api/v1/assets` - List digital assets
- `POST /api/v1/assets` - Upload digital content to mint an NFT
- `POST /api/v1/assets/{asset_id}/purchase` - Purchase an NFT
- `GET /api/v1/assets/{asset_id}` - Get asset details

## License

This project is licensed under the MIT License 