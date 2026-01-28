"""
Camera API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from datetime import datetime
import asyncio

from backend.models.auth import User
from backend.models.camera import CameraConfig, MotionEvent
from backend.core.security import get_current_active_user
from backend.services.camera_service import get_camera_service
from backend.services.discord_service import get_discord_notifier

router = APIRouter()


async def generate_mjpeg_stream(camera_id: int):
    """Generate MJPEG stream with motion detection"""
    camera_service = get_camera_service(camera_id)
    discord_notifier = await get_discord_notifier()
    
    recording_path = None
    frames_since_motion = 0
    max_frames_no_motion = 100  # Stop recording after ~5 seconds without motion (at 20fps)
    
    while True:
        try:
            # Get frame from camera
            frame_bytes = camera_service.get_frame()
            if frame_bytes is None:
                await asyncio.sleep(0.1)
                continue
            
            # Decode frame
            nparr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                continue
            
            # Adjust brightness/contrast
            frame = camera_service.adjust_frame(frame)
            
            # Detect motion
            motion_detected, confidence = camera_service.detect_motion(frame)
            
            if motion_detected:
                camera_service.motion_detected = True
                camera_service.last_motion_time = datetime.now()
                frames_since_motion = 0
                
                # Start recording if not already recording
                if not camera_service.is_recording:
                    recording_path = camera_service.start_recording(frame)
                    
                    # Save screenshot and send Discord notification
                    screenshot_path = camera_service.save_screenshot(frame)
                    await discord_notifier.send_motion_alert(
                        camera_id, 
                        confidence,
                        screenshot_path=screenshot_path,
                        recording_path=recording_path
                    )
            else:
                frames_since_motion += 1
            
            # Write frame to recording if active
            if camera_service.is_recording:
                camera_service.write_frame(frame)
                
                # Stop recording if no motion for a while
                if frames_since_motion > max_frames_no_motion:
                    camera_service.stop_recording()
                    camera_service.motion_detected = False
                    recording_path = None
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            
            # Yield frame in MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            await asyncio.sleep(0.05)  # ~20 fps
            
        except Exception as e:
            print(f"Error in stream generation: {e}")
            await asyncio.sleep(0.1)


@router.get("/stream/{camera_id}")
async def stream_camera(
    camera_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Stream camera feed with motion detection"""
    if camera_id not in [1, 2]:
        raise HTTPException(status_code=400, detail="Invalid camera ID")
    
    return StreamingResponse(
        generate_mjpeg_stream(camera_id),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/status/{camera_id}")
async def get_camera_status(
    camera_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Get camera status"""
    if camera_id not in [1, 2]:
        raise HTTPException(status_code=400, detail="Invalid camera ID")
    
    camera_service = get_camera_service(camera_id)
    
    return {
        "camera_id": camera_id,
        "is_recording": camera_service.is_recording,
        "motion_detected": camera_service.motion_detected,
        "last_motion_time": camera_service.last_motion_time.isoformat() if camera_service.last_motion_time else None,
        "sensitivity": camera_service.sensitivity,
        "brightness": camera_service.brightness,
        "contrast": camera_service.contrast
    }


@router.get("/list")
async def list_cameras(current_user: User = Depends(get_current_active_user)):
    """List all cameras"""
    return {
        "cameras": [
            {
                "id": 1,
                "name": "Camera 1",
                "status": "active"
            },
            {
                "id": 2,
                "name": "Camera 2",
                "status": "active"
            }
        ]
    }
