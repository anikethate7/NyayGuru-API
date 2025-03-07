from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from app.config import settings
from app.models.user import UserCreate
from app.models.schemas import TokenData, UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.database import get_db, User as DBUser

# Database operations
def get_user_by_email(db: Session, email: str) -> Optional[DBUser]:
    """Get a user by email."""
    return db.query(DBUser).filter(DBUser.email == email).first()

def create_user(db: Session, user: UserCreate) -> UserResponse:
    """Create a new user."""
    # Check if user already exists
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        id=str(uuid4()),
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Convert to response model
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active
    )

def authenticate_user(db: Session, email: str, password: str) -> Optional[DBUser]:
    """Authenticate a user."""
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user