# VisionGuard Quick Start Guide

Get VisionGuard up and running in 5 minutes! 🚀

## Prerequisites

✅ Docker and Docker Compose installed
✅ Two MJPEG-compatible webcams or IP cameras
✅ (Optional) Discord bot for notifications

## Step 1: Clone the Repository

```bash
git clone https://github.com/k4elis/VisionGuard.git
cd VisionGuard
```

## Step 2: Configure Your Cameras

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and update these essential settings:
```env
# Your camera MJPEG stream URLs
CAMERA1_URL=http://192.168.1.100:8080/video
CAMERA2_URL=http://192.168.1.101:8080/video

# Admin credentials (CHANGE THESE!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here

# Security keys (generate with: openssl rand -hex 32)
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

## Step 3: Start VisionGuard

### Option A: Using the Setup Script (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Using Docker Compose Directly
```bash
docker-compose up -d
```

### Option C: Using Make
```bash
make build
make up
```

## Step 4: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Step 5: Login

Use your configured credentials:
- Username: `admin` (or what you set in .env)
- Password: `admin123` (or what you set in .env)

## Step 6: Configure Your Cameras

1. Go to the **Settings** tab
2. Adjust motion sensitivity for each camera (0-100%)
3. Fine-tune brightness and contrast
4. Click "Apply Settings"

## Step 7: Monitor Your Cameras

1. Go to the **Live Cameras** tab
2. View real-time streams from both cameras
3. Motion detection runs automatically
4. Recordings are saved when motion is detected

## Step 8: View Recordings

1. Go to the **Recordings** tab
2. Browse captured videos and screenshots
3. Download or delete recordings

## Testing Without Real Cameras

If you don't have cameras yet, you can test with:

### Option 1: Use a Test MJPEG Stream
```bash
# Install FFmpeg
sudo apt-get install ffmpeg

# Create a test video file
ffmpeg -f lavfi -i testsrc=size=640x480:rate=25 -t 30 test.mp4

# Stream it as MJPEG (in another terminal)
ffmpeg -re -i test.mp4 -f mjpeg -listen 1 http://0.0.0.0:8080/video
```

Then set in `.env`:
```env
CAMERA1_URL=http://host.docker.internal:8080/video
CAMERA2_URL=http://host.docker.internal:8080/video
```

### Option 2: Use Your Phone as a Camera
1. Install "IP Webcam" (Android) or "IP Camera Lite" (iOS)
2. Start the server in the app
3. Use the provided URL in your `.env` file

### Option 3: Use Public Test Streams
Some public MJPEG streams for testing:
```env
# Note: These may not always be available
CAMERA1_URL=http://webcam.example.com/mjpeg
```

## Optional: Discord Notifications

### Step 1: Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Go to "Bot" section
4. Click "Add Bot"
5. Copy the bot token

### Step 2: Invite Bot to Server
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`
3. Select permissions: `Send Messages`, `Attach Files`
4. Copy and open the generated URL
5. Invite bot to your server

### Step 3: Get Channel ID
1. Enable Developer Mode in Discord (Settings → Advanced)
2. Right-click your channel
3. Click "Copy ID"

### Step 4: Update .env
```env
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### Step 5: Restart VisionGuard
```bash
docker-compose restart
```

## Common Issues

### Cameras Not Connecting
- ✅ Check camera URLs are correct
- ✅ Verify cameras are on same network
- ✅ Test URL in browser: `http://camera_ip:port/video`
- ✅ Check camera is in MJPEG mode (not H.264/RTSP)

### Port Already in Use
```bash
# Change ports in docker-compose.yml
ports:
  - "8080:80"      # Frontend on port 8080
  - "8001:8000"    # Backend on port 8001
```

### Can't Login
- ✅ Check credentials in `.env` file
- ✅ Ensure backend is running: `docker-compose logs backend`
- ✅ Clear browser cache

### High CPU Usage
- Lower motion sensitivity in Settings
- Reduce camera resolution
- Use lower frame rate cameras

## Development Mode

To run in development mode with hot-reload:
```bash
docker-compose -f docker-compose.dev.yml up
```

Or manually:
```bash
# Terminal 1: Backend
make dev-backend

# Terminal 2: Frontend
make dev-frontend
```

## Stopping VisionGuard

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

## Backup Recordings

```bash
# Create backup
tar -czf recordings_backup.tar.gz recordings/

# Restore backup
tar -xzf recordings_backup.tar.gz
```

## Update VisionGuard

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

## Need Help?

- 📖 Read the full [README.md](README.md)
- ⚙️ Check [CONFIGURATION.md](CONFIGURATION.md) for detailed settings
- 🔒 Review [SECURITY.md](SECURITY.md) for security best practices
- 🐛 Open an issue on GitHub

## Next Steps

Now that VisionGuard is running:

1. ✅ Change default credentials
2. ✅ Configure motion sensitivity
3. ✅ Set up Discord notifications
4. ✅ Test motion detection
5. ✅ Configure HTTPS for production
6. ✅ Set up automatic backups

Enjoy monitoring with VisionGuard! 🛡️
