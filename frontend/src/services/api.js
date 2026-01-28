import axios from 'axios';

const API_BASE_URL = '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (username, password) =>
    apiClient.post('/auth/login', { username, password }),
  getMe: () => apiClient.get('/auth/me'),
  logout: () => apiClient.post('/auth/logout'),
};

// Camera API
export const cameraAPI = {
  listCameras: () => apiClient.get('/cameras/list'),
  getStatus: (cameraId) => apiClient.get(`/cameras/status/${cameraId}`),
  getStreamUrl: (cameraId) => `${API_BASE_URL}/cameras/stream/${cameraId}`,
};

// Config API
export const configAPI = {
  updateSensitivity: (cameraId, sensitivity) =>
    apiClient.post('/config/sensitivity', { camera_id: cameraId, sensitivity }),
  updateCameraSettings: (cameraId, brightness, contrast) =>
    apiClient.post('/config/camera-settings', {
      camera_id: cameraId,
      brightness,
      contrast,
    }),
  getSettings: (cameraId) => apiClient.get(`/config/settings/${cameraId}`),
};

// Recordings API
export const recordingsAPI = {
  listRecordings: () => apiClient.get('/recordings/list'),
  downloadRecording: (filename) =>
    `${API_BASE_URL}/recordings/download/${filename}`,
  deleteRecording: (filename) =>
    apiClient.delete(`/recordings/delete/${filename}`),
};

export default apiClient;
