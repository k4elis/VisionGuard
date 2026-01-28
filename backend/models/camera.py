"""
Camera models
"""
from pydantic import BaseModel
from typing import Optional, Literal


class CameraConfig(BaseModel):
    """Camera configuration model"""
    camera_id: Literal[1, 2]
    url: str
    motion_sensitivity: int
    brightness: Optional[int] = None
    contrast: Optional[int] = None
    enabled: bool = True


class MotionEvent(BaseModel):
    """Motion detection event model"""
    camera_id: int
    timestamp: str
    confidence: float
    screenshot_path: Optional[str] = None
    recording_path: Optional[str] = None
