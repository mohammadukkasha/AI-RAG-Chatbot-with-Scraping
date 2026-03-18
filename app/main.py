from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.chat_routes import router as chat_router
from app.routes.website_routes import router as website_router
from app.database import connect_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(title="AI Chatbot — RAG + JWT + MongoDB", lifespan=lifespan)


# Routes
app.include_router(auth_router,    prefix="/api/auth",    tags=["Auth"])
app.include_router(website_router, prefix="/api/website", tags=["Website"])
app.include_router(chat_router,    prefix="/api/chat",    tags=["Chat"])


@app.get("/")
async def root():
    return {"status": "running", "version": "v2-groq-auth", "docs": "/docs"}