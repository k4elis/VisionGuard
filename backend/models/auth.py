"""
Authentication models
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


class User(BaseModel):
    """User model"""
    username: str
    disabled: Optional[bool] = None


class UserInDB(User):
    """User model with hashed password"""
    hashed_password: str


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str
