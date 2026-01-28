# VisionGuard 🛡️

![VisionGuard](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A professional video surveillance management system for MJPEG webcams with motion detection, automatic recording, and Discord notifications.

## 🌟 Features

### 1. **Real-time Video Streaming**
- Display of two MJPEG webcam feeds simultaneously
- Modern and ergonomic user interface
- Responsive design compatible with desktop and smartphone

### 2. **Motion Detection**
- Advanced motion detection algorithm using OpenCV
- Configurable sensitivity settings for each camera individually
- Real-time motion alerts

### 3. **Automatic Recording**
- Automatic video recording when motion is detected
- Local storage with date and time-based naming
- Recordings management interface

### 4. **Discord Notifications**
- Integration with Discord bot
- Automatic notifications on motion detection
- Screenshot attachments in notifications

### 5. **User Interface**
- Modern and clean design with Tailwind CSS
- Live camera feeds with status indicators
- Advanced settings panel for camera adjustments
- Recordings browser with download and delete options

### 6. **Security**
- JWT-based authentication system
- Password protection
- Session management
- Secure API endpoints

## 🏗️ Technology Stack

### Backend
- **Python 3.11** with FastAPI
- **OpenCV** for motion detection
- **discord.py** for Discord integration
- **Uvicorn** as ASGI server

### Frontend
- **React 18.2** with modern hooks
- **Tailwind CSS** for styling
- **Vite** as build tool
- **Lucide React** for icons

### Infrastructure
- **Docker** and Docker Compose for deployment
- **Nginx** as reverse proxy
- Environment-based configuration

## 📦 Installation

### Prerequisites
- Docker and Docker Compose installed
- MJPEG-compatible webcams or IP cameras
- Discord bot token (optional, for notifications)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/k4elis/VisionGuard.git
cd VisionGuard
```

2. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```env
# Camera URLs
CAMERA1_URL=http://192.168.1.100:8080/video
CAMERA2_URL=http://192.168.1.101:8080/video

# Motion Detection Sensitivity (0-100)
MOTION_SENSITIVITY_CAM1=50
MOTION_SENSITIVITY_CAM2=50

# Discord Configuration (optional)
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here

# Security Keys (generate secure keys!)
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

3. **Build and run with Docker**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Installation (Development)

#### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python main.py
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🎯 Usage

### Login
1. Navigate to http://localhost
2. Login with your admin credentials (default: admin / admin123)

### Dashboard
- **Live Cameras Tab**: View real-time streams from both cameras
- **Settings Tab**: Configure motion sensitivity, brightness, and contrast for each camera
- **Recordings Tab**: Browse, download, and delete recorded videos and screenshots

### Camera Configuration
Each camera can be configured individually:
- **Motion Sensitivity**: 0-100% (higher = more sensitive)
- **Brightness**: -100 to +100
- **Contrast**: -100 to +100

### Discord Notifications
When motion is detected:
1. A screenshot is captured
2. Video recording starts
3. Discord notification is sent with the screenshot
4. Recording continues until motion stops

## 🔧 API Documentation

### Authentication
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

### Cameras
- `GET /api/cameras/list` - List all cameras
- `GET /api/cameras/stream/{camera_id}` - Stream camera feed
- `GET /api/cameras/status/{camera_id}` - Get camera status

### Configuration
- `POST /api/config/sensitivity` - Update motion sensitivity
- `POST /api/config/camera-settings` - Update camera brightness/contrast
- `GET /api/config/settings/{camera_id}` - Get camera settings

### Recordings
- `GET /api/recordings/list` - List all recordings
- `GET /api/recordings/download/{filename}` - Download recording
- `DELETE /api/recordings/delete/{filename}` - Delete recording

## 📱 Mobile Support

VisionGuard is fully responsive and works on:
- Desktop browsers
- Tablets
- Smartphones

## 🔒 Security Recommendations

1. **Change default credentials** immediately after installation
2. **Generate secure secret keys** for JWT tokens
3. **Use HTTPS** in production (configure Nginx with SSL certificates)
4. **Restrict network access** to camera streams
5. **Regular backups** of recordings
6. **Keep dependencies updated**

## 🐳 Docker Deployment

### Production Deployment
```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Volumes
- `./recordings` - Stored video recordings and screenshots
- `./.env` - Environment configuration

## 🛠️ Development

### Project Structure
```
VisionGuard/
├── backend/
│   ├── api/          # API endpoints
│   ├── core/         # Core functionality (config, security)
│   ├── models/       # Data models
│   ├── services/     # Business logic (camera, discord)
│   └── utils/        # Utility functions
├── frontend/
│   ├── public/       # Static assets
│   └── src/
│       ├── components/  # React components
│       ├── contexts/    # React contexts
│       ├── pages/       # Page components
│       └── services/    # API services
├── recordings/       # Video recordings (auto-created)
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── requirements.txt
```

### Backend Technologies
- FastAPI for REST API
- OpenCV for image processing
- discord.py for bot integration
- JWT for authentication

### Frontend Technologies
- React with functional components and hooks
- Tailwind CSS for styling
- Axios for API calls
- React Router for navigation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Camera Connection Issues
- Verify camera URLs are correct and accessible
- Check that cameras support MJPEG protocol
- Ensure network connectivity between server and cameras

### Motion Detection Not Working
- Adjust sensitivity settings
- Check camera placement and lighting conditions
- Verify OpenCV installation

### Discord Notifications Not Sending
- Verify Discord bot token is valid
- Check that bot has permissions in the channel
- Ensure channel ID is correct

### Docker Issues
- Check logs: `docker-compose logs`
- Verify port availability (80, 8000)
- Ensure .env file exists and is configured

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/docs`

## 🎉 Acknowledgments

- FastAPI for the excellent web framework
- OpenCV for powerful image processing
- React and Tailwind CSS for modern UI development
- Discord.py for bot integration

---

Made with ❤️ for secure video surveillance