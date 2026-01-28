"""
Recordings API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import os
from datetime import datetime
from typing import List

from backend.models.auth import User
from backend.core.security import get_current_active_user
from backend.core.config import settings

router = APIRouter()


@router.get("/list")
async def list_recordings(current_user: User = Depends(get_current_active_user)):
    """List all recordings"""
    recordings_path = settings.RECORDINGS_PATH
    
    if not os.path.exists(recordings_path):
        return {"recordings": []}
    
    recordings = []
    for filename in os.listdir(recordings_path):
        if filename.endswith(('.mp4', '.avi', '.jpg')):
            filepath = os.path.join(recordings_path, filename)
            stat = os.stat(filepath)
            
            # Parse filename to extract info
            parts = filename.replace('.mp4', '').replace('.jpg', '').split('_')
            camera_id = parts[0].replace('camera', '') if len(parts) > 0 else 'unknown'
            
            recordings.append({
                "filename": filename,
                "camera_id": camera_id,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "type": "video" if filename.endswith(('.mp4', '.avi')) else "image"
            })
    
    # Sort by creation date (newest first)
    recordings.sort(key=lambda x: x['created'], reverse=True)
    
    return {"recordings": recordings}


@router.get("/download/{filename}")
async def download_recording(
    filename: str,
    current_user: User = Depends(get_current_active_user)
):
    """Download a recording"""
    # Security: Use basename to prevent path traversal
    filename = os.path.basename(filename)
    filepath = os.path.join(settings.RECORDINGS_PATH, filename)
    
    # Verify the file exists and is within the recordings directory
    recordings_path = os.path.abspath(settings.RECORDINGS_PATH)
    file_path = os.path.abspath(filepath)
    
    if not file_path.startswith(recordings_path):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return FileResponse(file_path, filename=filename)


@router.delete("/delete/{filename}")
async def delete_recording(
    filename: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a recording"""
    # Security: Use basename to prevent path traversal
    filename = os.path.basename(filename)
    filepath = os.path.join(settings.RECORDINGS_PATH, filename)
    
    # Verify the file exists and is within the recordings directory
    recordings_path = os.path.abspath(settings.RECORDINGS_PATH)
    file_path = os.path.abspath(filepath)
    
    if not file_path.startswith(recordings_path):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Recording not found")
    
    try:
        os.remove(file_path)
        return {"message": "Recording deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting recording: {str(e)}")
