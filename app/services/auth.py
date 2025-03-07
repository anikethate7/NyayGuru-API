from datetime import datetime
from uuid import uuid4
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.config import settings
from app.models.user import User, UserCreate, UserInDB
from app.models.schemas import TokenData
from app.utils.security import verify_password, get_password_hash
from app.database import get_db, User as DBUser

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_user_by_email(db: Session, email: str) -> Optional[DBUser]:
    """Get a user by email."""
    return db.query(DBUser).filter(DBUser.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user: User creation model
        
    Returns:
        Created user
    """
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
    
    # Convert to Pydantic model
    return User(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        created_at=db_user.created_at
    )

def authenticate_user(db: Session, email: str, password: str) -> Optional[DBUser]:
    """
    Authenticate a user.
    
    Args:
        db: Database session
        email: User email
        password: User password
        
    Returns:
        Authenticated user or None
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> DBUser:
    """
    Get the current authenticated user from token.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        Current user
    """
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
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user

def get_current_active_user(current_user: DBUser = Depends(get_current_user)) -> DBUser:
    """
    Get the current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user