import React, { useState, useEffect } from 'react';
import { configAPI } from '../services/api';
import { Settings, Sliders, Sun, Contrast } from 'lucide-react';

const SettingsPanel = () => {
  const [cam1Settings, setCam1Settings] = useState({
    sensitivity: 50,
    brightness: 0,
    contrast: 0,
  });
  const [cam2Settings, setCam2Settings] = useState({
    sensitivity: 50,
    brightness: 0,
    contrast: 0,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Load current settings
    const loadSettings = async () => {
      try {
        const [cam1Response, cam2Response] = await Promise.all([
          configAPI.getSettings(1),
          configAPI.getSettings(2),
        ]);
        setCam1Settings(cam1Response.data);
        setCam2Settings(cam2Response.data);
      } catch (err) {
        console.error('Error loading settings:', err);
      }
    };
    loadSettings();
  }, []);

  const handleSensitivityChange = async (cameraId, value) => {
    try {
      await configAPI.updateSensitivity(cameraId, value);
      if (cameraId === 1) {
        setCam1Settings({ ...cam1Settings, sensitivity: value });
      } else {
        setCam2Settings({ ...cam2Settings, sensitivity: value });
      }
      setMessage('Sensitivity updated successfully');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage('Error updating sensitivity');
    }
  };

  const handleCameraSettings = async (cameraId, brightness, contrast) => {
    setSaving(true);
    try {
      await configAPI.updateCameraSettings(cameraId, brightness, contrast);
      setMessage('Camera settings updated successfully');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage('Error updating camera settings');
    } finally {
      setSaving(false);
    }
  };

  const CameraSettingsCard = ({ cameraId, title, settings, setSettings }) => (
    <div className="glass-effect rounded-xl p-6 border border-slate-700">
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
        <Settings className="w-6 h-6 mr-2 text-blue-500" />
        {title}
      </h3>

      <div className="space-y-6">
        {/* Motion Sensitivity */}
        <div>
          <label className="flex items-center text-sm font-medium text-slate-300 mb-3">
            <Sliders className="w-4 h-4 mr-2" />
            Motion Sensitivity: {settings.sensitivity}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={settings.sensitivity}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              setSettings({ ...settings, sensitivity: value });
            }}
            onMouseUp={(e) => handleSensitivityChange(cameraId, parseInt(e.target.value))}
            onTouchEnd={(e) => handleSensitivityChange(cameraId, parseInt(e.target.value))}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
            style={{
              background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${settings.sensitivity}%, #334155 ${settings.sensitivity}%, #334155 100%)`,
            }}
          />
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>Less Sensitive</span>
            <span>More Sensitive</span>
          </div>
        </div>

        {/* Brightness */}
        <div>
          <label className="flex items-center text-sm font-medium text-slate-300 mb-3">
            <Sun className="w-4 h-4 mr-2" />
            Brightness: {settings.brightness > 0 ? '+' : ''}{settings.brightness}
          </label>
          <input
            type="range"
            min="-100"
            max="100"
            value={settings.brightness}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              setSettings({ ...settings, brightness: value });
            }}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>Darker</span>
            <span>Brighter</span>
          </div>
        </div>

        {/* Contrast */}
        <div>
          <label className="flex items-center text-sm font-medium text-slate-300 mb-3">
            <Contrast className="w-4 h-4 mr-2" />
            Contrast: {settings.contrast > 0 ? '+' : ''}{settings.contrast}
          </label>
          <input
            type="range"
            min="-100"
            max="100"
            value={settings.contrast}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              setSettings({ ...settings, contrast: value });
            }}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-1">
            <span>Less</span>
            <span>More</span>
          </div>
        </div>

        {/* Apply Button */}
        <button
          onClick={() =>
            handleCameraSettings(cameraId, settings.brightness, settings.contrast)
          }
          disabled={saving}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50"
        >
          {saving ? 'Applying...' : 'Apply Settings'}
        </button>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {message && (
        <div className="bg-green-900/50 border border-green-500 text-green-200 px-4 py-3 rounded-lg">
          {message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CameraSettingsCard
          cameraId={1}
          title="Camera 1 Settings"
          settings={cam1Settings}
          setSettings={setCam1Settings}
        />
        <CameraSettingsCard
          cameraId={2}
          title="Camera 2 Settings"
          settings={cam2Settings}
          setSettings={setCam2Settings}
        />
      </div>
    </div>
  );
};

export default SettingsPanel;
