# VisionGuard - Configuration Guide

## Environment Variables

### Required Configuration

#### Camera URLs
```env
CAMERA1_URL=http://192.168.1.100:8080/video
CAMERA2_URL=http://192.168.1.101:8080/video
```

**Setting up MJPEG cameras:**
- For IP cameras: Use the camera's MJPEG stream URL (check camera documentation)
- For USB cameras with DroidCam or similar apps: Use the provided stream URL
- Example formats:
  - `http://192.168.1.100:8080/video`
  - `http://192.168.1.100:8081/video.mjpeg`
  - `http://username:password@192.168.1.100:8080/video`

#### Motion Detection Sensitivity
```env
MOTION_SENSITIVITY_CAM1=50
MOTION_SENSITIVITY_CAM2=50
```
- Range: 0-100
- 0 = Least sensitive (only large movements)
- 100 = Most sensitive (detects small movements)
- Recommended: 40-60 for most scenarios

### Optional Configuration

#### Discord Bot Integration
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

**Setting up Discord bot:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Enable "Message Content Intent" if needed
6. Invite bot to your server with proper permissions
7. Get channel ID (right-click channel → Copy ID, enable Developer Mode in Discord settings)

#### Authentication
```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here
```
- Change default credentials immediately
- Use strong passwords in production

#### Security Keys
```env
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```
- Generate random secure keys
- Use different keys for each environment
- Command to generate: `openssl rand -hex 32`

#### Application Settings
```env
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

#### Recording Settings
```env
RECORDINGS_PATH=./recordings
MAX_RECORDING_DURATION=300
```
- `MAX_RECORDING_DURATION`: Maximum recording duration in seconds (default: 300 = 5 minutes)

## Camera Compatibility

### Supported Formats
- MJPEG (Motion JPEG) streams
- HTTP-based streams
- IP cameras with MJPEG support

### Tested Cameras
- Generic USB webcams with DroidCam, IP Webcam apps
- Hikvision IP cameras (MJPEG mode)
- Dahua IP cameras (MJPEG mode)
- Generic RTSP cameras converted to MJPEG

### Converting RTSP to MJPEG
If your camera only supports RTSP, you can use FFmpeg:
```bash
ffmpeg -i rtsp://camera_ip:554/stream -f mjpeg http://localhost:8080/video
```

## Network Configuration

### Port Requirements
- **80**: Frontend (Nginx)
- **8000**: Backend API
- **Custom**: Camera stream ports (as configured)

### Firewall Rules
Ensure these ports are accessible:
```bash
# Allow frontend
sudo ufw allow 80/tcp

# Allow backend API
sudo ufw allow 8000/tcp

# Allow camera connections (adjust based on your network)
sudo ufw allow from 192.168.1.0/24
```

## Performance Tuning

### Motion Detection
- Lower sensitivity = Better performance, fewer false positives
- Higher sensitivity = More detections, higher CPU usage

### Recording Settings
- Reduce `MAX_RECORDING_DURATION` for shorter clips
- Increase for longer continuous recording

### Camera Resolution
Lower resolution streams = Better performance:
- 640x480 (VGA) - Best performance
- 1280x720 (HD) - Balanced
- 1920x1080 (Full HD) - Best quality, higher resource usage

## Troubleshooting

### Camera Not Connecting
1. Test camera URL in browser: `http://camera_ip:port/video`
2. Check network connectivity: `ping camera_ip`
3. Verify camera credentials in URL if required
4. Check firewall settings

### High CPU Usage
1. Reduce motion detection sensitivity
2. Lower camera resolution
3. Increase frame skip in motion detection
4. Use hardware acceleration if available

### Discord Notifications Not Working
1. Verify bot token is correct
2. Check bot has permissions in channel
3. Ensure channel ID is correct
4. Check bot is online in Discord server

### Storage Issues
1. Set up automatic cleanup for old recordings
2. Monitor disk space: `df -h`
3. Configure recording retention policy

## Security Best Practices

### Production Deployment
1. Use HTTPS with valid SSL certificates
2. Change all default credentials
3. Use strong, unique passwords
4. Generate secure JWT secret keys
5. Restrict network access to cameras
6. Enable firewall rules
7. Regular security updates

### SSL/HTTPS Setup with Let's Encrypt
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Backup and Recovery

### Backup Recordings
```bash
# Manual backup
tar -czf recordings_backup_$(date +%Y%m%d).tar.gz recordings/

# Automated backup (add to crontab)
0 2 * * * tar -czf /backup/recordings_$(date +\%Y\%m\%d).tar.gz /app/recordings/
```

### Database Backup (if using)
```bash
# Backup configuration
cp .env .env.backup
```

## Monitoring

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Check Status
```bash
# Service status
docker-compose ps

# Resource usage
docker stats
```

## Scaling

### Multiple Camera Support
To add more cameras:
1. Add camera URLs to `.env`
2. Modify backend to support additional cameras
3. Update frontend to display additional streams

### Load Balancing
For high-traffic scenarios:
1. Use multiple backend instances
2. Configure load balancer (Nginx, HAProxy)
3. Use Redis for session storage
4. Consider CDN for static assets
