from fastapi import APIRouter, HTTPException, Depends
from app.schemas import WebsiteData
from app.scraper import scrape_website
from app.embeddings import generate_embeddings
from app.rag_pipeline import store_embeddings
from app.database import websites_collection
from app.core.security import get_current_user
from datetime import datetime

router = APIRouter()


@router.post("/add-website")
async def add_website(
    body: WebsiteData,
    current_user: dict = Depends(get_current_user)  
):
    url_str = str(body.url)

 
    try:
        text = scrape_website(url_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Website scrape nahi hui: {str(e)}")

    if not text:
        raise HTTPException(status_code=400, detail="Website pe koi content nahi mila")

    
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = generate_embeddings(chunks)
    store_embeddings(chunks, embeddings)

  
    record = {
        "user_id": str(current_user["_id"]),
        "username": current_user["username"],
        "url": url_str,
        "status": "processed",
        "chunks": len(chunks),
        "created_at": datetime.now()
    }
    result = await websites_collection.insert_one(record)

    return {
        "id": str(result.inserted_id),
        "message": "Website successfully process ho gayi ",
        "url": url_str,
        "chunks": len(chunks),
        "scraped_by": current_user["username"]
    }


@router.get("/my-websites")
async def my_websites(current_user: dict = Depends(get_current_user)):
    """Current user ki saari scraped websites"""

    cursor = websites_collection.find({"user_id": str(current_user["_id"])})
    websites = []
    async for doc in cursor:
        websites.append({
            "id": str(doc["_id"]),
            "url": doc["url"],
            "status": doc["status"],
            "chunks": doc["chunks"],
            "created_at": str(doc["created_at"])
        })

    return {"websites": websites, "total": len(websites)}