import React, { useState } from 'react';
import axios from 'axios';

function AISuggestions({ content, analysisResults }) {
  const [suggestions, setSuggestions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rewriteMode, setRewriteMode] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [rewriteGoal, setRewriteGoal] = useState('improve readability and engagement');
  const [rewrittenText, setRewrittenText] = useState('');

  const handleGetSuggestions = async () => {
    if (!content || !analysisResults) {
      alert('Please run an analysis first');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/ai/suggestions', {
        content,
        analysis_results: analysisResults
      });

      setSuggestions(response.data);
    } catch (err) {
      console.error('Error getting AI suggestions:', err);
      alert('Failed to get AI suggestions');
    } finally {
      setLoading(false);
    }
  };

  const handleRewrite = async () => {
    if (!selectedText) {
      alert('Please enter text to rewrite');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/ai/rewrite', {
        text: selectedText,
        goal: rewriteGoal,
        context: content
      });

      setRewrittenText(response.data.rewritten);
    } catch (err) {
      console.error('Error rewriting:', err);
      alert('Failed to rewrite text');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-4 sm:p-8 border border-slate-100 mt-8">
      <div className="flex flex-col md:flex-row justify-between items-start gap-4 mb-6">
        <div>
          <h3 className="text-2xl font-bold text-slate-800 mb-2">AI Content Improvements</h3>
          <p className="text-slate-600">Get AI-powered suggestions to fix weak areas</p>
        </div>
        
        <div className="flex flex-wrap gap-2 w-full md:w-auto">
          <button
            onClick={() => setRewriteMode(!rewriteMode)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              rewriteMode
                ? 'bg-purple-600 text-white'
                : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
            }`}
          >
            {rewriteMode ? 'View Suggestions' : 'Rewrite Tool'}
          </button>
          
          {!rewriteMode && (
            <button
              onClick={handleGetSuggestions}
              disabled={loading}
              className={`px-6 py-2 rounded-lg font-medium transition-all ${
                loading
                  ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:shadow-lg active:scale-95'
              }`}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Get AI Suggestions
                </span>
              )}
            </button>
          )}
        </div>
      </div>

      {!rewriteMode ? (
        // Suggestions View
        suggestions ? (
          <div className="space-y-6">
            {suggestions.status === 'excellent' ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
                <div className="text-green-800 font-semibold text-lg">{suggestions.message}</div>
              </div>
            ) : (
              <>
                {/* Priority Actions */}
                {suggestions.priority_actions && suggestions.priority_actions.length > 0 && (
                  <div className="bg-gradient-to-r from-orange-50 to-red-50 border border-orange-200 rounded-lg p-6">
                    <h4 className="text-lg font-bold text-orange-900 mb-4 flex items-center gap-2">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                      Priority Actions
                    </h4>
                    <div className="space-y-3">
                      {suggestions.priority_actions.map((action, idx) => (
                        <div key={idx} className="bg-white p-4 rounded-lg border border-orange-200">
                          <div className="font-semibold text-orange-900 mb-1">{action.area}</div>
                          <div className="text-sm text-slate-700 mb-2">{action.action}</div>
                          <div className="flex gap-2 text-xs">
                            <span className="px-2 py-1 bg-red-100 text-red-700 rounded">Impact: {action.impact}</span>
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">Effort: {action.effort}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Detailed Suggestions by Area */}
                {suggestions.suggestions && suggestions.suggestions.map((sugg, idx) => (
                  <div key={idx} className="border border-slate-200 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-bold text-slate-800">{sugg.area}</h4>
                      <div className="flex items-center gap-2">
                        <span className="text-2xl font-bold text-slate-600">{sugg.score}/100</span>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          sugg.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                        }`}>
                          {sugg.priority} priority
                        </span>
                      </div>
                    </div>

                    {/* Issues */}
                    {sugg.issues && sugg.issues.length > 0 && (
                      <div className="mb-4">
                        <h5 className="font-semibold text-red-700 text-sm mb-2">Issues:</h5>
                        <ul className="space-y-1">
                          {sugg.issues.map((issue, i) => (
                            <li key={i} className="text-sm text-red-600 flex items-start gap-2">
                              <span className="text-red-400 mt-0.5">✗</span>
                              <span>{issue}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* AI Suggestions */}
                    {sugg.ai_suggestions && sugg.ai_suggestions.length > 0 && (
                      <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg border border-purple-200">
                        <h5 className="font-semibold text-purple-900 text-sm mb-3 flex items-center gap-2">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                          </svg>
                          AI Recommendations:
                        </h5>
                        <ul className="space-y-2">
                          {sugg.ai_suggestions.map((rec, i) => (
                            <li key={i} className="text-sm text-slate-700 pl-3 border-l-2 border-purple-400">
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </>
            )}
          </div>
        ) : (
          <div className="text-center py-12 text-slate-500">
            <svg className="w-16 h-16 mx-auto mb-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <p>Click "Get AI Suggestions" to receive personalized improvement recommendations</p>
          </div>
        )
      ) : (
        // Rewrite Tool View
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Text to Rewrite
            </label>
            <textarea
              value={selectedText}
              onChange={(e) => setSelectedText(e.target.value)}
              placeholder="Paste the section you want to improve..."
              rows={6}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Improvement Goal
            </label>
            <select
              value={rewriteGoal}
              onChange={(e) => setRewriteGoal(e.target.value)}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            >
              <option value="improve readability and engagement">Improve Readability & Engagement</option>
              <option value="make more professional and authoritative">Make More Professional</option>
              <option value="simplify for beginners">Simplify for Beginners</option>
              <option value="add more detail and examples">Add More Detail & Examples</option>
              <option value="make more concise and direct">Make More Concise</option>
            </select>
          </div>

          <button
            onClick={handleRewrite}
            disabled={loading || !selectedText}
            className={`w-full px-6 py-3 rounded-lg font-medium transition-all ${
              loading || !selectedText
                ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:shadow-lg active:scale-95'
            }`}
          >
            {loading ? 'Rewriting...' : 'Rewrite with AI'}
          </button>

          {rewrittenText && (
            <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-6">
              <div className="flex justify-between items-start mb-3">
                <h4 className="font-semibold text-green-900">Improved Version:</h4>
                <button
                  onClick={() => copyToClipboard(rewrittenText)}
                  className="px-3 py-1 bg-white border border-green-300 text-green-700 rounded text-sm hover:bg-green-50"
                >
                  Copy
                </button>
              </div>
              <p className="text-slate-700 whitespace-pre-wrap">{rewrittenText}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AISuggestions;
