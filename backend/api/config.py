"""
Configuration API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.models.auth import User
from backend.models.camera import CameraConfig
from backend.core.security import get_current_active_user
from backend.services.camera_service import get_camera_service

router = APIRouter()


class SensitivityUpdate(BaseModel):
    """Model for sensitivity update"""
    camera_id: int
    sensitivity: int


class CameraSettings(BaseModel):
    """Model for camera settings"""
    camera_id: int
    brightness: int
    contrast: int


@router.post("/sensitivity")
async def update_sensitivity(
    update: SensitivityUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update motion detection sensitivity"""
    if update.camera_id not in [1, 2]:
        raise HTTPException(status_code=400, detail="Invalid camera ID")
    
    if not 0 <= update.sensitivity <= 100:
        raise HTTPException(status_code=400, detail="Sensitivity must be between 0 and 100")
    
    camera_service = get_camera_service(update.camera_id)
    camera_service.sensitivity = update.sensitivity
    
    return {
        "message": "Sensitivity updated",
        "camera_id": update.camera_id,
        "sensitivity": update.sensitivity
    }


@router.post("/camera-settings")
async def update_camera_settings(
    settings: CameraSettings,
    current_user: User = Depends(get_current_active_user)
):
    """Update camera brightness and contrast"""
    if settings.camera_id not in [1, 2]:
        raise HTTPException(status_code=400, detail="Invalid camera ID")
    
    if not -100 <= settings.brightness <= 100:
        raise HTTPException(status_code=400, detail="Brightness must be between -100 and 100")
    
    if not -100 <= settings.contrast <= 100:
        raise HTTPException(status_code=400, detail="Contrast must be between -100 and 100")
    
    camera_service = get_camera_service(settings.camera_id)
    camera_service.brightness = settings.brightness
    camera_service.contrast = settings.contrast
    
    return {
        "message": "Camera settings updated",
        "camera_id": settings.camera_id,
        "brightness": settings.brightness,
        "contrast": settings.contrast
    }


@router.get("/settings/{camera_id}")
async def get_camera_settings(
    camera_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get camera settings"""
    if camera_id not in [1, 2]:
        raise HTTPException(status_code=400, detail="Invalid camera ID")
    
    camera_service = get_camera_service(camera_id)
    
    return {
        "camera_id": camera_id,
        "sensitivity": camera_service.sensitivity,
        "brightness": camera_service.brightness,
        "contrast": camera_service.contrast
    }
