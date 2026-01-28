"""
Authentication API endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.models.auth import Token, User, LoginRequest
from backend.core.security import (
    authenticate_user,
    create_access_token,
    get_current_active_user
)
from backend.core.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Login endpoint"""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout endpoint (client-side token removal)"""
    return {"message": "Successfully logged out"}
