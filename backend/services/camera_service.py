"""
Camera service for handling MJPEG streams and motion detection
"""
import cv2
import numpy as np
from typing import Optional, Tuple
import requests
from io import BytesIO
from PIL import Image
import threading
import time
from datetime import datetime
import os

from backend.core.config import settings


class CameraService:
    """Service for handling camera operations"""
    
    def __init__(self, camera_id: int, url: str, sensitivity: int = 50):
        self.camera_id = camera_id
        self.url = url
        self.sensitivity = sensitivity
        self.previous_frame = None
        self.is_recording = False
        self.motion_detected = False
        self.last_motion_time = None
        self.recording_writer = None
        self.brightness = 0
        self.contrast = 0
        
    def get_frame(self) -> Optional[bytes]:
        """Get a single frame from the MJPEG stream"""
        try:
            response = requests.get(self.url, stream=True, timeout=5)
            if response.status_code == 200:
                bytes_data = bytes()
                for chunk in response.iter_content(chunk_size=1024):
                    bytes_data += chunk
                    # Find JPEG boundaries
                    a = bytes_data.find(b'\xff\xd8')  # JPEG start
                    b = bytes_data.find(b'\xff\xd9')  # JPEG end
                    if a != -1 and b != -1:
                        jpg = bytes_data[a:b+2]
                        bytes_data = bytes_data[b+2:]
                        return jpg
        except Exception as e:
            print(f"Error getting frame from camera {self.camera_id}: {e}")
            return None
        return None
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        Detect motion in the frame
        Returns: (motion_detected, confidence)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Initialize previous frame
        if self.previous_frame is None:
            self.previous_frame = gray
            return False, 0.0
        
        # Compute difference
        frame_delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calculate motion level
        motion_level = 0
        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Minimum area threshold
                continue
            motion_level += cv2.contourArea(contour)
        
        # Update previous frame
        self.previous_frame = gray
        
        # Calculate confidence based on sensitivity
        threshold = (100 - self.sensitivity) * 1000
        confidence = min(motion_level / threshold, 1.0) if threshold > 0 else 0.0
        motion_detected = motion_level > threshold
        
        return motion_detected, confidence
    
    def start_recording(self, frame: np.ndarray) -> str:
        """Start recording video"""
        if self.is_recording:
            return None
        
        # Create recordings directory
        os.makedirs(settings.RECORDINGS_PATH, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"camera{self.camera_id}_{timestamp}.mp4"
        filepath = os.path.join(settings.RECORDINGS_PATH, filename)
        
        # Initialize video writer
        height, width = frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.recording_writer = cv2.VideoWriter(filepath, fourcc, 20.0, (width, height))
        
        self.is_recording = True
        return filepath
    
    def write_frame(self, frame: np.ndarray):
        """Write frame to recording"""
        if self.is_recording and self.recording_writer is not None:
            self.recording_writer.write(frame)
    
    def stop_recording(self):
        """Stop recording video"""
        if self.is_recording and self.recording_writer is not None:
            self.recording_writer.release()
            self.recording_writer = None
            self.is_recording = False
    
    def save_screenshot(self, frame: np.ndarray) -> str:
        """Save a screenshot of the frame"""
        os.makedirs(settings.RECORDINGS_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"camera{self.camera_id}_{timestamp}.jpg"
        filepath = os.path.join(settings.RECORDINGS_PATH, filename)
        cv2.imwrite(filepath, frame)
        return filepath
    
    def adjust_frame(self, frame: np.ndarray) -> np.ndarray:
        """Adjust frame brightness and contrast"""
        if self.brightness != 0 or self.contrast != 0:
            # Adjust brightness and contrast
            alpha = 1.0 + self.contrast / 100.0  # Contrast control
            beta = self.brightness  # Brightness control
            frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        return frame


# Global camera instances
camera_services = {}


def get_camera_service(camera_id: int) -> CameraService:
    """Get or create camera service instance"""
    if camera_id not in camera_services:
        url = settings.CAMERA1_URL if camera_id == 1 else settings.CAMERA2_URL
        sensitivity = settings.MOTION_SENSITIVITY_CAM1 if camera_id == 1 else settings.MOTION_SENSITIVITY_CAM2
        camera_services[camera_id] = CameraService(camera_id, url, sensitivity)
    return camera_services[camera_id]
