# Crypto Asset Marketplace Backend

A robust FastAPI backend for a digital asset marketplace, supporting NFT-style asset management, user authentication, admin controls, and seamless file uploads to Cloudinary. Built with MongoDB (via Beanie ODM), JWT authentication, and a modular, scalable architecture.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [User Endpoints](#user-endpoints)
  - [Admin Endpoints](#admin-endpoints)
  - [Asset Endpoints](#asset-endpoints)
- [Database Models](#database-models)
- [Cloudinary Integration](#cloudinary-integration)
- [Authentication & Authorization](#authentication--authorization)
- [License](#license)

---

## Features

- User registration, login, and JWT-based authentication
- User profile management
- Admin user management (CRUD, activate/deactivate)
- Digital asset upload (image, video, PDF) with duplicate detection
- Asset listing, retrieval, update, and deletion
- File storage and delivery via Cloudinary
- Category and asset type management
- Secure, modular, and extensible codebase

---

## Tech Stack

- **FastAPI** (Python 3.8+)
- **MongoDB** (with Beanie ODM)
- **Cloudinary** (file storage)
- **JWT** (authentication)
- **PyMongo**, **Pydantic**, **Uvicorn**

---

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── api_v1/
│   │   │   ├── auth/      # Authentication endpoints
│   │   │   ├── users/     # User endpoints
│   │   │   ├── admin/     # Admin endpoints
│   │   │   ├── asset/     # Asset endpoints
│   │   ├── router.py      # API router aggregation
│   ├── core/              # Config, security, settings
│   ├── models/            # Database models (Beanie Documents)
│   ├── schemas/           # Pydantic schemas for API
│   ├── services/          # Business logic
│   ├── utils/             # Helpers, Cloudinary integration
│   ├── main.py            # FastAPI app entrypoint
├── requirements.txt       # Python dependencies
```

---

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (local or hosted)
- Cloudinary account (for file uploads)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in `backend/` with the following (replace with your values):

   ```
   MONGO_CONNECTION_STRING=mongodb+srv://<user>:<pass>@<cluster>/<db>
   DATABASE_NAME=nft_marketplace
   JWT_SECRET_KEY=your_jwt_secret
   JWT_SECRET_REFRESH_KEY=your_refresh_secret
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Endpoints

### Authentication

| Method | Path              | Description                | Request Body / Params         | Response Example |
|--------|-------------------|----------------------------|-------------------------------|------------------|
| POST   | `/api/v1/auth/login`   | Login, get JWT tokens         | `username`, `password` (form) | `{ "access_token": "...", "refresh_token": "...", "token_type": "bearer" }` |
| POST   | `/api/v1/auth/refresh` | Refresh access token          | `refresh_token` (string)      | `{ "access_token": "...", "refresh_token": "...", "token_type": "bearer" }` |

#### Example: Login

```json
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username: user@example.com
password: yourpassword
```

#### Example: Refresh

```json
POST /api/v1/auth/refresh
{
  "refresh_token": "<refresh_token>"
}
```

---

### User Endpoints

| Method | Path                | Description                | Auth Required | Request Body / Params | Response Example |
|--------|---------------------|----------------------------|---------------|----------------------|------------------|
| POST   | `/api/v1/users/create` | Register new user           | No            | `{ "email": "...", "username": "...", "password": "..." }` | User object |
| GET    | `/api/v1/users/me`     | Get current user profile    | Yes           | -                    | User object      |
| PUT    | `/api/v1/users/update` | Update user profile         | Yes           | `{ "username": "...", "password": "..." }` | User object |

#### User Object Example

```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "user",
  "disabled": false,
  "created_at": "2024-06-01T12:00:00"
}
```

---

### Admin Endpoints

> **All admin endpoints require an authenticated admin user.**

| Method | Path                                 | Description                | Request Body / Params | Response Example |
|--------|--------------------------------------|----------------------------|----------------------|------------------|
| GET    | `/api/v1/admin/admin`                | Admin test route           | -                    | `{ "message": "...", "user": {...} }` |
| GET    | `/api/v1/admin/users`                | List all users             | -                    | `[User, ...]`    |
| GET    | `/api/v1/admin/users/{user_id}`      | Get user by ID             | -                    | User object      |
| DELETE | `/api/v1/admin/users/{user_id}`      | Delete user by ID          | -                    | `{ "message": "User deleted successfully" }` |
| POST   | `/api/v1/admin/users/{user_id}/activate`   | Activate user              | -                    | `{ "message": "User activated successfully" }` |
| POST   | `/api/v1/admin/users/{user_id}/deactivate` | Deactivate user            | -                    | `{ "message": "User deactivated successfully" }` |

---

### Asset Endpoints

> **All asset endpoints require authentication.**

| Method | Path                        | Description                | Request Body / Params | Response Example |
|--------|-----------------------------|----------------------------|----------------------|------------------|
| POST   | `/api/v1/asset/`            | Upload new asset (file)    | Multipart form: `file`, `title`, `description`, `price`, `category` (JSON list), `metadata` (JSON) | Asset object |
| GET    | `/api/v1/asset/getall`      | List all assets            | -                    | `[Asset, ...]`   |
| GET    | `/api/v1/asset/{user_id}`   | List assets for user       | -                    | `[Asset, ...]`   |
| GET    | `/api/v1/asset/get/{asset_id}` | Get asset by ID           | -                    | Asset object     |
| PUT    | `/api/v1/asset/{asset_id}`  | Update asset               | JSON: fields to update | Asset object  |
| DELETE | `/api/v1/asset/{asset_id}`  | Delete asset               | -                    | `{ "message": "Asset deleted successfully" }` |

#### Asset Object Example

```json
{
  "asset_id": "uuid",
  "title": "My Art",
  "description": "A beautiful digital painting",
  "price": 1.5,
  "categories": ["art", "collectibles"],
  "file_url": "https://res.cloudinary.com/...",
  "owner_id": "uuid",
  "created_at": "2024-06-01T12:00:00",
  "updated_at": null,
  "metadata": { "resolution": "4k" }
}
```

---

## Database Models

### User (`users` collection)

- `user_id` (UUID, unique)
- `username` (string, unique)
- `email` (string, unique)
- `hashed_password` (string)
- `profile_picture_url` (string, optional)
- `disabled` (bool)
- `created_at` (datetime)
- `is_admin` (bool)

### Asset (`assets` collection)

- `asset_id` (UUID, unique)
- `title` (string)
- `description` (string, optional)
- `asset_type` (int, references asset_types)
- `file_url` (string, Cloudinary URL)
- `price` (float)
- `owner_id` (UUID, references users)
- `category_ids` (list of int, references categories)
- `content_hash` (string, for duplicate detection)
- `metadata` (dict, optional)
- `is_minted` (bool)
- `token_id` (string, optional)
- `created_at` (datetime)
- `updated_at` (datetime, optional)

### Category (`categories` collection)

- `category_id` (int, unique)
- `name` (enum: art, music, photography, collectibles, gaming, sports, virtual_real_estate)

### AssetType (`asset_types` collection)

- `asset_type_id` (int, unique)
- `name` (string: image, video, pdf)

---

## Cloudinary Integration

- All asset files (images, videos, PDFs) are uploaded directly to Cloudinary.
- Duplicate detection is performed before upload (using perceptual hash for images, content hash for others).
- The `file_url` field in the asset object is a direct Cloudinary link.
- Cloudinary credentials are required in your environment variables.

---

## Authentication & Authorization

- JWT-based authentication (access and refresh tokens).
- Use the `Authorization: Bearer <token>` header for all protected endpoints.
- Admin endpoints require the user to have `is_admin: true`.
- Passwords are securely hashed.

---

## License

This project is licensed under the MIT License.

---

**For questions or contributions, please open an issue or pull request!**
