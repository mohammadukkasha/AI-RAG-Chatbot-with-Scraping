import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def check():
    load_dotenv()
    url = os.getenv("MONGODB_URL")
    print(f"Connecting to: {url[:20]}...")
    client = AsyncIOMotorClient(url)
    db = client["ai_chatbot"]
    try:
        print("Pinging...")
        await client.admin.command("ping")
        print("Ping successful!")
        
        print("Checking users count...")
        count = await db.users.count_documents({})
        print(f"Users count: {count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check())
