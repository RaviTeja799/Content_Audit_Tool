import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

function AdminPanel() {
  const [clearing, setClearing] = useState(false);
  const [message, setMessage] = useState('');

  const handleClearData = async () => {
    if (!window.confirm('Are you sure you want to delete ALL analysis results, history, and batch data? This action cannot be undone.')) {
      return;
    }

    setClearing(true);
    setMessage('');

    try {
      const response = await axios.post(`${API_URL}/api/clear-data`);
      setMessage({
        type: 'success',
        text: response.data.message || 'All data has been cleared successfully'
      });
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to clear data. Please try again.'
      });
    } finally {
      setClearing(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-100 mt-8">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Admin Tools</h3>
          <p className="text-sm text-slate-600 mt-1">Manage application data</p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h4 className="font-semibold text-red-900 mb-2">Clear All Data</h4>
          <p className="text-sm text-red-700 mb-4">
            Remove all analysis results, history, and batch data. This action cannot be undone.
          </p>
          <button
            onClick={handleClearData}
            disabled={clearing}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              clearing
                ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                : 'bg-red-600 text-white hover:bg-red-700 active:scale-95'
            }`}
          >
            {clearing ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Clearing...
              </span>
            ) : (
              'Clear All Data'
            )}
          </button>
        </div>

        {message && (
          <div className={`p-4 rounded-lg border ${
            message.type === 'success'
              ? 'bg-green-50 border-green-200 text-green-800'
              : 'bg-red-50 border-red-200 text-red-800'
          }`}>
            <p className="text-sm font-medium">{message.text}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminPanel;
