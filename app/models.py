# MongoDB document schemas (for reference only)
# MongoDB is schema-less, so these are just documentation of the expected document structure.
# Actual validation is handled by Pydantic schemas in schemas.py

"""
User Document:
{
    "_id": ObjectId,
    "username": str,
    "email": str,
    "password": str (hashed),
    "created_at": datetime
}

Website Document:
{
    "_id": ObjectId,
    "user_id": str,
    "username": str,
    "url": str,
    "status": str,
    "chunks": int,
    "created_at": datetime
}

ChatHistory Document:
{
    "_id": ObjectId,
    "user_id": str,
    "username": str,
    "message": str,
    "response": str,
    "mode": str,
    "timestamp": datetime
}
"""