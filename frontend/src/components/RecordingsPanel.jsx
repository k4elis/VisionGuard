import React, { useState, useEffect } from 'react';
import { recordingsAPI } from '../services/api';
import { FileVideo, Download, Trash2, Image, Video as VideoIcon, Calendar, HardDrive } from 'lucide-react';

const RecordingsPanel = () => {
  const [recordings, setRecordings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  useEffect(() => {
    loadRecordings();
  }, []);

  const loadRecordings = async () => {
    try {
      const response = await recordingsAPI.listRecordings();
      setRecordings(response.data.recordings);
    } catch (err) {
      console.error('Error loading recordings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm('Are you sure you want to delete this recording?')) {
      return;
    }

    setDeleting(filename);
    try {
      await recordingsAPI.deleteRecording(filename);
      setRecordings(recordings.filter((r) => r.filename !== filename));
    } catch (err) {
      alert('Error deleting recording');
    } finally {
      setDeleting(null);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  if (loading) {
    return (
      <div className="glass-effect rounded-xl p-8 text-center">
        <div className="text-slate-400">Loading recordings...</div>
      </div>
    );
  }

  if (recordings.length === 0) {
    return (
      <div className="glass-effect rounded-xl p-8 text-center">
        <FileVideo className="w-16 h-16 text-slate-600 mx-auto mb-4" />
        <p className="text-slate-400 text-lg">No recordings yet</p>
        <p className="text-slate-500 text-sm mt-2">
          Recordings will appear here when motion is detected
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="glass-effect rounded-xl p-6 border border-slate-700">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
          <FileVideo className="w-7 h-7 mr-2 text-blue-500" />
          Recordings ({recordings.length})
        </h2>

        <div className="grid grid-cols-1 gap-4">
          {recordings.map((recording) => (
            <div
              key={recording.filename}
              className="bg-slate-800/50 rounded-lg p-4 border border-slate-700 hover:border-slate-600 transition duration-200"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  {/* Icon */}
                  <div
                    className={`p-3 rounded-lg ${
                      recording.type === 'video'
                        ? 'bg-blue-900/50 text-blue-400'
                        : 'bg-green-900/50 text-green-400'
                    }`}
                  >
                    {recording.type === 'video' ? (
                      <VideoIcon className="w-6 h-6" />
                    ) : (
                      <Image className="w-6 h-6" />
                    )}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">
                      {recording.filename}
                    </p>
                    <div className="flex items-center space-x-4 mt-1 text-sm text-slate-400">
                      <span className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {new Date(recording.created).toLocaleString()}
                      </span>
                      <span className="flex items-center">
                        <HardDrive className="w-4 h-4 mr-1" />
                        {formatFileSize(recording.size)}
                      </span>
                      <span className="bg-blue-900/50 text-blue-400 px-2 py-0.5 rounded text-xs">
                        Camera {recording.camera_id}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center space-x-2">
                  <a
                    href={recordingsAPI.downloadRecording(recording.filename)}
                    download
                    className="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition duration-200"
                    title="Download"
                  >
                    <Download className="w-5 h-5" />
                  </a>
                  <button
                    onClick={() => handleDelete(recording.filename)}
                    disabled={deleting === recording.filename}
                    className="p-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition duration-200 disabled:opacity-50"
                    title="Delete"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RecordingsPanel;
