from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request model."""
    query: str = Field(..., description="User's question")
    category: str = Field(..., description="Legal category")
    language: str = Field("English", description="Response language")
    session_id: str = Field(..., description="Unique session identifier")
    messages: Optional[List[Message]] = Field(None, description="Previous messages in the conversation")


class ChatResponse(BaseModel):
    """Chat response model."""
    answer: str = Field(..., description="Answer to the user's question")
    sources: Optional[List[str]] = Field(None, description="Sources of information")


class CategoryResponse(BaseModel):
    """Category response model."""
    categories: List[str] = Field(..., description="Available legal categories")


class LanguageResponse(BaseModel):
    """Language response model."""
    languages: Dict[str, str] = Field(..., description="Available languages with their codes")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field("ok", description="API status")
    version: str = Field(..., description="API version")