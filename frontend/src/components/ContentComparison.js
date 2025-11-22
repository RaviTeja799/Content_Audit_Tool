import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

function ContentComparison({ content, keyword, metadata }) {
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCompare = async () => {
    if (!content || !keyword) {
      setError('Please provide both content and target keyword');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await axios.post(`${API_URL}/api/compare-content`, {
        content: content,
        keyword: keyword,
        metadata: metadata || {}
      });

      setComparison(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to compare content');
      console.error('Content comparison error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getGapScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getGapScoreBg = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 60) return 'bg-blue-50 border-blue-200';
    if (score >= 40) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-slate-100 mt-8">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="text-2xl font-bold text-slate-800 mb-2">Content Comparison</h3>
          <p className="text-slate-600">Compare your content with the top-ranking competitor</p>
        </div>
        
        <button
          onClick={handleCompare}
          disabled={loading || !content || !keyword}
          className={`
            px-6 py-2.5 rounded-lg font-medium transition-all duration-200
            ${loading || !content || !keyword
              ? 'bg-slate-300 text-slate-500 cursor-not-allowed' 
              : 'bg-indigo-600 text-white hover:bg-indigo-700 hover:shadow-md active:scale-95'
            }
          `}
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Comparing...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Compare with #1
            </span>
          )}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {comparison && (
        <div className="space-y-6">
          {/* Gap Score */}
          <div className={`p-6 rounded-lg border-2 ${getGapScoreBg(comparison.gap_score)}`}>
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-lg font-semibold text-slate-800 mb-1">Competitive Gap Score</h4>
                <p className="text-slate-600">{comparison.interpretation}</p>
              </div>
              <div className={`text-5xl font-bold ${getGapScoreColor(comparison.gap_score)}`}>
                {comparison.gap_score}/100
              </div>
            </div>
          </div>

          {/* Competitor Info */}
          <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
            <h5 className="font-semibold text-slate-700 mb-2">Comparing Against:</h5>
            <a 
              href={comparison.competitor_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 font-medium truncate block"
            >
              {comparison.competitor_title}
            </a>
            <p className="text-sm text-slate-500 mt-1 truncate">{comparison.competitor_url}</p>
          </div>

          {/* Structural Comparison */}
          <div>
            <h4 className="text-lg font-semibold text-slate-800 mb-3">Structural Comparison</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <div className="text-blue-600 text-sm font-medium mb-2">Word Count</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-blue-900">
                    {comparison.structural_gaps.word_count.yours.toLocaleString()}
                  </span>
                  <span className="text-sm text-blue-700">
                    vs {comparison.structural_gaps.word_count.competitor.toLocaleString()}
                  </span>
                </div>
                <div className="mt-2 text-sm">
                  <span className={`font-semibold ${comparison.structural_gaps.word_count.gap > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {comparison.structural_gaps.word_count.gap > 0 ? '-' : '+'}{Math.abs(comparison.structural_gaps.word_count.gap)} words
                  </span>
                  <span className="text-slate-600 ml-2">
                    ({comparison.structural_gaps.word_count.percentage}%)
                  </span>
                </div>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <div className="text-purple-600 text-sm font-medium mb-2">Headers</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-purple-900">
                    {comparison.structural_gaps.headers.yours}
                  </span>
                  <span className="text-sm text-purple-700">
                    vs {comparison.structural_gaps.headers.competitor}
                  </span>
                </div>
                {comparison.structural_gaps.headers.gap !== 0 && (
                  <div className="mt-2 text-sm">
                    <span className={`font-semibold ${comparison.structural_gaps.headers.gap > 0 ? 'text-red-600' : 'text-green-600'}`}>
                      {comparison.structural_gaps.headers.gap > 0 ? 'Add' : 'Excellent'} {Math.abs(comparison.structural_gaps.headers.gap)} more
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Topic Coverage */}
          <div>
            <h4 className="text-lg font-semibold text-slate-800 mb-3">Topic Coverage</h4>
            <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-lg border border-indigo-200 mb-4">
              <div className="flex items-center justify-between">
                <span className="text-indigo-700 font-medium">Content Similarity</span>
                <span className="text-2xl font-bold text-indigo-900">{comparison.topic_gaps.similarity}%</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                <h5 className="font-semibold text-red-700 mb-3">Missing Topics (Add These)</h5>
                <ul className="space-y-2">
                  {comparison.topic_gaps.unique_to_competitor.length > 0 ? (
                    comparison.topic_gaps.unique_to_competitor.map((topic, idx) => (
                      <li key={idx} className="text-sm text-red-600 flex items-start gap-2">
                        <span className="text-red-400 mt-0.5">✗</span>
                        <span>{topic}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-sm text-slate-500 italic">No missing topics - excellent coverage!</li>
                  )}
                </ul>
              </div>

              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <h5 className="font-semibold text-green-700 mb-3">Your Unique Topics</h5>
                <ul className="space-y-2">
                  {comparison.topic_gaps.unique_to_you.length > 0 ? (
                    comparison.topic_gaps.unique_to_you.map((topic, idx) => (
                      <li key={idx} className="text-sm text-green-600 flex items-start gap-2">
                        <span className="text-green-400 mt-0.5">✓</span>
                        <span>{topic}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-sm text-slate-500 italic">No unique topics yet</li>
                  )}
                </ul>
              </div>
            </div>
          </div>

          {/* Content Elements */}
          <div>
            <h4 className="text-lg font-semibold text-slate-800 mb-3">Content Elements</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(comparison.element_gaps).map(([element, data]) => (
                <div 
                  key={element}
                  className={`p-4 rounded-lg border-2 ${
                    data.gap 
                      ? 'bg-red-50 border-red-200' 
                      : data.yours 
                        ? 'bg-green-50 border-green-200' 
                        : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div className="text-xs text-slate-600 uppercase mb-1 font-medium">{element}</div>
                  <div className={`text-2xl font-bold ${
                    data.gap ? 'text-red-600' : data.yours ? 'text-green-600' : 'text-slate-400'
                  }`}>
                    {data.yours ? '✓' : '✗'}
                  </div>
                  {data.gap && (
                    <div className="text-xs text-red-600 mt-1">Missing</div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          <div>
            <h4 className="text-lg font-semibold text-slate-800 mb-3">Action Plan</h4>
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
              <ul className="space-y-3">
                {comparison.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                      {idx + 1}
                    </span>
                    <span className="text-slate-800 font-medium">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Readability */}
          {comparison.readability_comparison.your_readability > 0 && (
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
              <h5 className="font-semibold text-slate-700 mb-2">Readability</h5>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-slate-600">Your Score:</span>
                  <span className="ml-2 font-bold text-slate-800">{comparison.readability_comparison.your_readability}</span>
                </div>
                <div>
                  <span className="text-slate-600">Competitor Score:</span>
                  <span className="ml-2 font-bold text-slate-800">{comparison.readability_comparison.competitor_readability}</span>
                </div>
              </div>
              <p className="text-xs text-slate-500 mt-2">
                Your content is {comparison.readability_comparison.comparison} to read than the competitor
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ContentComparison;
