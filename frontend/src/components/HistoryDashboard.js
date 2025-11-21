import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function HistoryDashboard() {
  const [history, setHistory] = useState([]);
  const [progress, setProgress] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [historyRes, progressRes, statsRes] = await Promise.all([
        axios.get('http://localhost:5000/api/history', { params: { limit: 10 } }),
        axios.get('http://localhost:5000/api/history/progress', { params: { days: 30 } }),
        axios.get('http://localhost:5000/api/history/statistics')
      ]);

      setHistory(historyRes.data);
      setProgress(progressRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  if (loading && !stats) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 border border-slate-100">
        <div className="flex items-center justify-center">
          <div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full"></div>
          <span className="ml-3 text-slate-600">Loading history...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200">
            <div className="text-blue-600 text-sm font-medium mb-2">Total Analyses</div>
            <div className="text-4xl font-bold text-blue-900">{stats.total_analyses}</div>
          </div>
          
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200">
            <div className="text-green-600 text-sm font-medium mb-2">Average Score</div>
            <div className="text-4xl font-bold text-green-900">{stats.avg_scores.overall}/100</div>
          </div>
          
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200">
            <div className="text-purple-600 text-sm font-medium mb-2">Top Keyword</div>
            <div className="text-lg font-bold text-purple-900 truncate">
              {stats.top_keywords[0]?.keyword || 'N/A'}
            </div>
          </div>
        </div>
      )}

      {/* Progress Chart */}
      {progress.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-100">
          <h3 className="text-xl font-bold text-slate-800 mb-4">Score Progress Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={progress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" tickFormatter={formatDate} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="overall_score" stroke="#3b82f6" name="Overall" strokeWidth={2} />
              <Line type="monotone" dataKey="seo_score" stroke="#10b981" name="SEO" />
              <Line type="monotone" dataKey="serp_score" stroke="#8b5cf6" name="SERP" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Recent History */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-100">
        <h3 className="text-xl font-bold text-slate-800 mb-4">Recent Analyses</h3>
        <div className="space-y-3">
          {history.map((item) => (
            <div key={item.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-200 hover:bg-slate-100 transition-colors gap-2">
              <div className="flex-1 w-full">
                <div className="font-semibold text-slate-800 truncate">
                  {item.target_keyword || item.url || 'Untitled'}
                </div>
                <div className="text-sm text-slate-500">
                  {formatDate(item.created_at)} • {item.word_count} words
                </div>
              </div>
              <div className="text-2xl font-bold text-primary-600 self-end sm:self-auto">
                {item.overall_score}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HistoryDashboard;
