import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

function KeywordResearch({ targetKeyword }) {
  const [keywords, setKeywords] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleResearch = async () => {
    if (!targetKeyword) {
      setError('Please enter a target keyword first');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await axios.post(`${API_URL}/api/research-keywords`, {
        keyword: targetKeyword,
        max_results: 20
      });

      setKeywords(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to research keywords');
      console.error('Keyword research error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    if (difficulty < 30) return 'text-green-600 bg-green-50';
    if (difficulty < 60) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getDifficultyLabel = (difficulty) => {
    if (difficulty < 30) return 'Easy';
    if (difficulty < 60) return 'Medium';
    return 'Hard';
  };

  const getOpportunityColor = (score) => {
    if (score >= 70) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 50) return 'text-blue-600 bg-blue-50 border-blue-200';
    return 'text-slate-600 bg-slate-50 border-slate-200';
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-slate-100">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="text-2xl font-bold text-slate-800 mb-2">Keyword Research</h3>
          <p className="text-slate-600">Discover related keywords and content opportunities</p>
        </div>
        
        <button
          onClick={handleResearch}
          disabled={loading || !targetKeyword}
          className={`
            px-6 py-2.5 rounded-lg font-medium transition-all duration-200
            ${loading || !targetKeyword
              ? 'bg-slate-300 text-slate-500 cursor-not-allowed' 
              : 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-md active:scale-95'
            }
          `}
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Researching...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Research Keywords
            </span>
          )}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {keywords && (
        <div className="space-y-6">
          {/* Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
              <div className="text-blue-600 text-sm font-medium mb-1">Total Keywords</div>
              <div className="text-3xl font-bold text-blue-900">{keywords.total_keywords}</div>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
              <div className="text-green-600 text-sm font-medium mb-1">Seed Keyword</div>
              <div className="text-lg font-bold text-green-900 truncate">{keywords.seed_keyword}</div>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
              <div className="text-purple-600 text-sm font-medium mb-1">Intent Types</div>
              <div className="text-3xl font-bold text-purple-900">{Object.keys(keywords.categories).length}</div>
            </div>
          </div>

          {/* Keywords Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="text-left p-3 font-semibold text-slate-700">Keyword</th>
                  <th className="text-center p-3 font-semibold text-slate-700">Volume</th>
                  <th className="text-center p-3 font-semibold text-slate-700">Difficulty</th>
                  <th className="text-center p-3 font-semibold text-slate-700">Opportunity</th>
                  <th className="text-center p-3 font-semibold text-slate-700">Intent</th>
                  <th className="text-center p-3 font-semibold text-slate-700">Type</th>
                </tr>
              </thead>
              <tbody>
                {keywords.keywords.map((kw, index) => (
                  <tr key={index} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                    <td className="p-3">
                      <span className="font-medium text-slate-800">{kw.keyword}</span>
                    </td>
                    <td className="p-3 text-center">
                      <span className="text-slate-700">{kw.search_volume.toLocaleString()}</span>
                    </td>
                    <td className="p-3 text-center">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getDifficultyColor(kw.difficulty)}`}>
                        {getDifficultyLabel(kw.difficulty)}
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className={`px-3 py-1 rounded-full text-sm font-bold border ${getOpportunityColor(kw.opportunity_score)}`}>
                        {kw.opportunity_score}/100
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className="text-xs px-2 py-1 bg-slate-100 text-slate-600 rounded capitalize">
                        {kw.intent}
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className="text-xs text-slate-500 capitalize">{kw.type}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Intent Categories */}
          <div className="mt-6">
            <h4 className="text-lg font-semibold text-slate-800 mb-3">Keywords by Intent</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(keywords.categories).map(([intent, kws]) => (
                <div key={intent} className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                  <h5 className="font-semibold text-slate-700 mb-2 capitalize">{intent}</h5>
                  <ul className="space-y-1">
                    {kws.slice(0, 5).map((kw, idx) => (
                      <li key={idx} className="text-sm text-slate-600 truncate">• {kw}</li>
                    ))}
                  </ul>
                  {kws.length > 5 && (
                    <p className="text-xs text-slate-500 mt-2">+{kws.length - 5} more</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default KeywordResearch;
