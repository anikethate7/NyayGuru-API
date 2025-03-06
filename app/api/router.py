from fastapi import APIRouter

from app.api.endpoints import chat, categories

# Create main API router
api_router = APIRouter()

# Include specific endpoint routers
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])