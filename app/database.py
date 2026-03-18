from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URL, DB_NAME

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

users_collection        = db["users"]
websites_collection     = db["websites"]
chat_history_collection = db["chat_history"]


async def connect_db():
    try:
        await client.admin.command("ping")
        print("MongoDB Atlas connected!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")


async def close_db():
    client.close()