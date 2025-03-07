from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user import UserCreate, User, UserLogin
from app.models.schemas import Token, SignupResponse, LoginResponse, UserResponse
from app.services.auth import create_user, authenticate_user, get_current_active_user
from app.utils.security import create_access_token
from app.database import get_db, User as DBUser

router = APIRouter()

@router.post("/signup", response_model=SignupResponse)
async def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: User email address
    - **password**: User password (min 8 characters)
    - **full_name**: User's full name (optional)
    """
    # Create user
    user = create_user(db, user_create)
    
    # Convert to response model
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active
    )
    
    return SignupResponse(user=user_response)


@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and generate access token.
    
    - **username**: User email address
    - **password**: User password
    """
    # Authenticate user
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token
    access_token = create_access_token(subject=user.email)
    
    # Convert to response model
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active
    )
    
    return LoginResponse(
        access_token=access_token,
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: DBUser = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active
    )