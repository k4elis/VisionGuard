import React, { useState, useEffect } from 'react';
import { cameraAPI } from '../services/api';
import { Video, Circle, Play, AlertTriangle } from 'lucide-react';

const CameraView = ({ cameraId, title }) => {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(false);
  const token = localStorage.getItem('token');

  useEffect(() => {
    // Fetch camera status periodically
    const fetchStatus = async () => {
      try {
        const response = await cameraAPI.getStatus(cameraId);
        setStatus(response.data);
      } catch (err) {
        console.error('Error fetching camera status:', err);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, [cameraId]);

  const streamUrl = `${cameraAPI.getStreamUrl(cameraId)}?token=${token}`;

  return (
    <div className="glass-effect rounded-xl overflow-hidden border border-slate-700">
      {/* Header */}
      <div className="bg-slate-800/50 px-4 py-3 border-b border-slate-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Video className="w-5 h-5 text-blue-500 mr-2" />
            <h3 className="text-lg font-semibold text-white">{title}</h3>
          </div>
          <div className="flex items-center space-x-4">
            {status?.motion_detected && (
              <div className="flex items-center">
                <Circle className="w-3 h-3 text-red-500 fill-current animate-pulse mr-2" />
                <span className="text-red-500 text-sm font-medium">Motion Detected</span>
              </div>
            )}
            {status?.is_recording && (
              <div className="flex items-center">
                <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse mr-2"></div>
                <span className="text-red-500 text-sm font-medium">Recording</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Video Stream */}
      <div className="relative bg-slate-900 aspect-video">
        {!error ? (
          <img
            src={streamUrl}
            alt={title}
            className="w-full h-full object-contain"
            onError={() => setError(true)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-center">
              <AlertTriangle className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
              <p className="text-slate-400 mb-2">Unable to connect to camera</p>
              <p className="text-slate-500 text-sm">Check camera URL in settings</p>
              <button
                onClick={() => setError(false)}
                className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition duration-200"
              >
                Retry
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer Info */}
      {status && (
        <div className="bg-slate-800/50 px-4 py-3 border-t border-slate-700">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Sensitivity:</span>
              <span className="ml-2 text-white font-medium">{status.sensitivity}%</span>
            </div>
            <div>
              <span className="text-slate-400">Last Motion:</span>
              <span className="ml-2 text-white font-medium">
                {status.last_motion_time
                  ? new Date(status.last_motion_time).toLocaleTimeString()
                  : 'None'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CameraView;
