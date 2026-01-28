import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Shield, LogOut, Settings, Video, FileVideo, AlertCircle } from 'lucide-react';
import CameraView from '../components/CameraView';
import SettingsPanel from '../components/SettingsPanel';
import RecordingsPanel from '../components/RecordingsPanel';

const DashboardPage = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('cameras');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <nav className="glass-effect border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-blue-500" />
              <span className="ml-2 text-xl font-bold text-white">VisionGuard</span>
            </div>

            <div className="flex items-center space-x-4">
              <span className="text-slate-300">Welcome, {user?.username}</span>
              <button
                onClick={logout}
                className="flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition duration-200"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="flex space-x-4 border-b border-slate-700">
          <button
            onClick={() => setActiveTab('cameras')}
            className={`flex items-center px-4 py-3 font-medium transition duration-200 ${
              activeTab === 'cameras'
                ? 'text-blue-500 border-b-2 border-blue-500'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Video className="w-5 h-5 mr-2" />
            Live Cameras
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`flex items-center px-4 py-3 font-medium transition duration-200 ${
              activeTab === 'settings'
                ? 'text-blue-500 border-b-2 border-blue-500'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Settings className="w-5 h-5 mr-2" />
            Settings
          </button>
          <button
            onClick={() => setActiveTab('recordings')}
            className={`flex items-center px-4 py-3 font-medium transition duration-200 ${
              activeTab === 'recordings'
                ? 'text-blue-500 border-b-2 border-blue-500'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileVideo className="w-5 h-5 mr-2" />
            Recordings
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'cameras' && (
          <div className="space-y-6">
            <div className="glass-effect p-4 rounded-lg border border-yellow-600/50 bg-yellow-900/20">
              <div className="flex items-start">
                <AlertCircle className="w-5 h-5 text-yellow-500 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <h3 className="text-yellow-500 font-semibold mb-1">Camera Configuration Required</h3>
                  <p className="text-slate-300 text-sm">
                    Please configure your camera URLs in the <code className="bg-slate-800 px-1 py-0.5 rounded">.env</code> file.
                    Set <code className="bg-slate-800 px-1 py-0.5 rounded">CAMERA1_URL</code> and{' '}
                    <code className="bg-slate-800 px-1 py-0.5 rounded">CAMERA2_URL</code> to your MJPEG stream URLs.
                  </p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <CameraView cameraId={1} title="Camera 1" />
              <CameraView cameraId={2} title="Camera 2" />
            </div>
          </div>
        )}

        {activeTab === 'settings' && <SettingsPanel />}
        {activeTab === 'recordings' && <RecordingsPanel />}
      </div>
    </div>
  );
};

export default DashboardPage;
