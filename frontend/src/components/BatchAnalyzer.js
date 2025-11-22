import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

function BatchAnalyzer() {
  const [urls, setUrls] = useState('');
  const [batchName, setBatchName] = useState('');
  const [batchId, setBatchId] = useState(null);
  const [batchStatus, setBatchStatus] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const handleCreateBatch = async () => {
    const urlList = urls.split('\n').filter(u => u.trim());
    
    if (urlList.length === 0) {
      alert('Please enter at least one URL');
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/batch/create`, {
        name: batchName || `Batch Analysis ${new Date().toLocaleString()}`,
        urls: urlList
      });

      setBatchId(response.data.batch_id);
      startBatchAnalysis(response.data.batch_id, urlList);
    } catch (err) {
      console.error('Error creating batch:', err);
      alert('Failed to create batch');
    }
  };

  const startBatchAnalysis = async (bId, urlList) => {
    setAnalyzing(true);

    for (const url of urlList) {
      try {
        await axios.post(`${API_URL}/api/batch/analyze`, {
          batch_id: bId,
          url: url.trim(),
          target_keyword: ''
        });
      } catch (err) {
        console.error(`Error analyzing ${url}:`, err);
      }

      // Fetch updated status
      const statusRes = await axios.get(`${API_URL}/api/batch/status/${bId}`);
      setBatchStatus(statusRes.data);
    }

    setAnalyzing(false);
  };

  const exportResults = () => {
    if (!batchStatus) return;

    const csvContent = [
      ['URL', 'Status', 'Overall Score', 'SEO', 'SERP', 'AEO', 'Humanization', 'Differentiation'].join(','),
      ...batchStatus.items.map(item => [
        item.url,
        item.status,
        item.overall_score || 'N/A',
        '', '', '', '', ''  // Would need to fetch full results for these
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `batch-analysis-${batchId}.csv`;
    a.click();
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-slate-100">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-slate-800 mb-2">Batch Analysis</h3>
        <p className="text-slate-600">Analyze multiple URLs at once for efficient auditing</p>
      </div>

      {!batchId ? (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Batch Name (Optional)
            </label>
            <input
              type="text"
              value={batchName}
              onChange={(e) => setBatchName(e.target.value)}
              placeholder="My Website Audit"
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              URLs (One per line)
            </label>
            <textarea
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              placeholder="https://example.com/page1&#10;https://example.com/page2&#10;https://example.com/page3"
              rows={8}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent font-mono text-sm"
            />
          </div>

          <button
            onClick={handleCreateBatch}
            className="w-full px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 hover:shadow-md transition-all active:scale-95"
          >
            Start Batch Analysis
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-blue-900">Batch ID: {batchId}</span>
              {analyzing && (
                <span className="flex items-center text-blue-600">
                  <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing...
                </span>
              )}
            </div>
            {batchStatus && (
              <div className="text-blue-700">
                Progress: {batchStatus.completed_urls} / {batchStatus.total_urls} URLs
              </div>
            )}
          </div>

          {batchStatus && (
            <>
              <div className="space-y-2">
                {batchStatus.items.map((item, idx) => (
                  <div key={idx} className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200 gap-2">
                    <div className="flex-1 truncate w-full">
                      <span className="text-sm text-slate-700 block truncate">{item.url}</span>
                    </div>
                    <div className="flex items-center gap-3 self-end sm:self-auto">
                      {item.status === 'completed' && (
                        <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                          {item.overall_score}/100
                        </span>
                      )}
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        item.status === 'completed' ? 'bg-green-100 text-green-700' :
                        item.status === 'failed' ? 'bg-red-100 text-red-700' :
                        'bg-yellow-100 text-yellow-700'
                      }`}>
                        {item.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {batchStatus.status === 'completed' && (
                <button
                  onClick={exportResults}
                  className="w-full px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 hover:shadow-md transition-all active:scale-95"
                >
                  Export Results as CSV
                </button>
              )}

              <button
                onClick={() => {
                  setBatchId(null);
                  setBatchStatus(null);
                  setUrls('');
                }}
                className="w-full px-6 py-3 bg-slate-600 text-white rounded-lg font-medium hover:bg-slate-700 transition-all"
              >
                Start New Batch
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default BatchAnalyzer;
