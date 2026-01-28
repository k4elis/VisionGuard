"""
VisionGuard - Professional Video Surveillance System
Main application entry point
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
import os
from dotenv import load_dotenv

from backend.api import auth, cameras, config, recordings
from backend.core.config import settings

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="VisionGuard",
    description="Professional Video Surveillance System with Motion Detection",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if "*" in origins:
    print("WARNING: CORS is configured to allow all origins. This should be changed in production!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(cameras.router, prefix="/api/cameras", tags=["Cameras"])
app.include_router(config.router, prefix="/api/config", tags=["Configuration"])
app.include_router(recordings.router, prefix="/api/recordings", tags=["Recordings"])

# Serve static files for recordings
if os.path.exists("./recordings"):
    app.mount("/recordings", StaticFiles(directory="./recordings"), name="recordings")

# Serve frontend in production
if os.path.exists("./frontend/build"):
    app.mount("/", StaticFiles(directory="./frontend/build", html=True), name="frontend")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VisionGuard API",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
