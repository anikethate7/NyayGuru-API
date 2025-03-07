from fastapi import APIRouter

from app.api.endpoints import chat, categories, auth
from app.config import settings

# Create main API router
api_router = APIRouter()

# Include specific endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Dynamically create category-specific routes
category_router = APIRouter()
for category in settings.LEGAL_CATEGORIES:
    # Create a route for each category
    normalized_category = category.lower().replace(" ", "-")
    api_router.include_router(
        chat.router,
        prefix=f"/{normalized_category}",
        tags=[f"{category}"]
    )