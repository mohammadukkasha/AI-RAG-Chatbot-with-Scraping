from fastapi import APIRouter, HTTPException, status
from app.schemas import RegisterSchema, LoginSchema, TokenSchema
from app.database import users_collection
from app.core.security import hash_password, verify_password, create_access_token
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/register", status_code=201)
async def register(body: RegisterSchema):

    existing = await users_collection.find_one({"email": body.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    existing_username = await users_collection.find_one({"username": body.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    user = {
        "username": body.username,
        "email": body.email,
        "password": hash_password(body.password),
        "session_id": str(uuid.uuid4()),
        "created_at": datetime.now()
    }
    await users_collection.insert_one(user)

    return {"message": "Account created! Please login."}


@router.post("/login", response_model=TokenSchema)
async def login(body: LoginSchema):

    user = await users_collection.find_one({"email": body.email})

    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    new_session_id = str(uuid.uuid4())
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"session_id": new_session_id}}
    )

    access_token = create_access_token(data={"sub": user["email"], "sid": new_session_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }