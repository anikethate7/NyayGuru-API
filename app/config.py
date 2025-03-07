import os
import secrets
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "LawGPT"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    
    # Google API settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # GROQ API settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Vector database settings
    VECTOR_STORE_PATH: str = "my_vector_store"
    
    # Embedding model settings
    EMBEDDING_MODEL: str = "models/embedding-001"

    # Add this in your Settings class
    VITE_API_URL: str = os.getenv("VITE_API_URL", "http://localhost:5000/api")

    
    # LLM settings
    LLM_MODEL: str = "llama3-70b-8192"
    
    # Translation settings
    ENABLE_TRANSLATION: bool = True
    
    # Supported languages
    SUPPORTED_LANGUAGES: dict = {
        "English": "en",
        "Hindi": "hi",
        "Marathi": "mr",
    }
    
    # Legal categories
    LEGAL_CATEGORIES: List[str] = [
        "Know Your Rights",
        "Criminal Law",
        "Cyber Law",
        "Property Law",
        "Consumer Law",
    ]
    
    # Chunk size for document splitting
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Retrieval settings
    RETRIEVAL_K: int = 4
    
    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lawgpt.db")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()