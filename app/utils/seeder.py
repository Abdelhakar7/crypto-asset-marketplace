# scripts/seed_asset_types.py

import asyncio
from models.asset_type import AssetType

PREDEFINED_TYPES = [
    {"asset_type_id": 1, "name": "image"},
    {"asset_type_id": 2, "name": "video"},
    {"asset_type_id": 3, "name": "pdf"},
]

async def seed():
    # if collection already has docs, skip
    if await AssetType.count() > 0:
        print("✅ asset_types already seeded")
        return

    for t in PREDEFINED_TYPES:
        await AssetType.insert_one(t)
        print(f"  • inserted {t}")

    print("✅ asset_types seeded")

if __name__ == "__main__":
    asyncio.run(seed())
