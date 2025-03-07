import os
from typing import Generator
from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, User as DBUser
from app.models.schemas import TokenData

# Set environment variables
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@lru_cache
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Get Google Generative AI embeddings with caching."""
    return GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL)

@lru_cache
def get_vector_store() -> FAISS:
    """Load vector store from disk with caching."""
    embeddings = get_embeddings()
    return FAISS.load_local(
        settings.VECTOR_STORE_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )

def get_retriever():
    """Get vector store retriever."""
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": settings.RETRIEVAL_K}
    )

def get_llm():
    """Get LLM model."""
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY, 
        model_name=settings.LLM_MODEL
    )

def get_conversation_memory(session_id: str) -> ConversationBufferWindowMemory:
    """Get conversation memory for a session."""
    return ConversationBufferWindowMemory(
        k=2, 
        memory_key="chat_history", 
        return_messages=True,
        output_key="answer"
    )

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> DBUser:
    """Get current authenticated user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(DBUser).filter(DBUser.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: DBUser = Depends(get_current_user)) -> DBUser:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user