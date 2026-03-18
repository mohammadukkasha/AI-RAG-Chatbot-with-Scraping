from fastapi import APIRouter, Depends
from app.schemas import ChatMessage
from app.rag_pipeline import rag_answer
from app.database import chat_history_collection
from app.core.security import get_current_user
from datetime import datetime

router = APIRouter()


@router.post("/chat")
async def chat(
    body: ChatMessage,
    current_user: dict = Depends(get_current_user)   
):
    try:
        answer = rag_answer(body.message)

        if answer and not answer.startswith("Error"):
            mode = "website"
        elif answer and answer.startswith("Error"):
             mode = "error"
        else:
            answer = "Mujhe is topic ka koi context nahi mila. Pehle website add karo."
            mode = "general"
    except Exception as e:
        answer = f"System Error: {str(e)}"
        mode = "error"

    record = {
        "user_id": str(current_user["_id"]),
        "username": current_user["username"],
        "message": body.message,
        "response": answer,
        "mode": mode,
        "timestamp": datetime.now()
    }
    result = await chat_history_collection.insert_one(record)

    return {
        "id": str(result.inserted_id),
        "response": answer,
        "mode": mode,
        "asked_by": current_user["username"]
    }


@router.get("/my-chats")
async def my_chats(current_user: dict = Depends(get_current_user)):
    """Current user ki saari chat history"""

    cursor = chat_history_collection.find(
        {"user_id": str(current_user["_id"])}
    ).sort("timestamp", -1).limit(50)

    chats = []
    async for doc in cursor:
        chats.append({
            "id": str(doc["_id"]),
            "message": doc["message"],
            "response": doc["response"],
            "mode": doc["mode"],
            "timestamp": str(doc["timestamp"])
        })

    return {"chats": chats, "total": len(chats)}