"""
Core configuration settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "*"  # Comma-separated list of allowed origins
    
    # Camera URLs
    CAMERA1_URL: str = "http://192.168.1.100:8080/video"
    CAMERA2_URL: str = "http://192.168.1.101:8080/video"
    
    # Motion Detection
    MOTION_SENSITIVITY_CAM1: int = 50
    MOTION_SENSITIVITY_CAM2: int = 50
    
    # Discord
    DISCORD_BOT_TOKEN: Optional[str] = None
    DISCORD_CHANNEL_ID: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "change_me_in_production"
    JWT_SECRET_KEY: str = "change_me_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin Credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change_me_in_production"
    
    # Recordings
    RECORDINGS_PATH: str = "./recordings"
    MAX_RECORDING_DURATION: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
