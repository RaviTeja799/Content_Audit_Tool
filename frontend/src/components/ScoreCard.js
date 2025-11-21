import React, { useState } from 'react';

function ScoreCard({ title, data, color }) {
  const [expanded, setExpanded] = useState(false);

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Work';
    return 'Poor';
  };

  const getScoreColorClass = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getScoreTextColorClass = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const colorClasses = {
    blue: 'border-t-blue-500',
    indigo: 'border-t-indigo-500',
    emerald: 'border-t-emerald-500',
    amber: 'border-t-amber-500',
    pink: 'border-t-pink-500',
  };

  return (
    <div className={`bg-white rounded-xl shadow-md border border-slate-100 border-t-4 ${colorClasses[color] || 'border-t-slate-500'} p-6 transition-all hover:shadow-lg`}>
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-slate-800">
          {title}
        </h3>
        <div className={`px-4 py-1 rounded-full text-white font-bold text-sm ${getScoreColorClass(data.score)}`}>
          {data.score}/100
        </div>
      </div>

      <div className="mb-6">
        <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden">
          <div 
            className={`h-full ${getScoreColorClass(data.score)} transition-all duration-1000 ease-out`}
            style={{ width: `${data.score}%` }}
          ></div>
        </div>
        <div className={`text-right mt-1 text-sm font-medium ${getScoreTextColorClass(data.score)}`}>
          {getScoreLabel(data.score)}
        </div>
      </div>

      <div className="space-y-6">
        {/* Good Points */}
        {data.good_points && data.good_points.length > 0 && (
          <div>
            <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-2">
              <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
              Strengths
            </h4>
            <ul className="space-y-2">
              {data.good_points.map((point, index) => (
                <li key={index} className="text-sm text-slate-600 flex items-start gap-2">
                  <span className="text-green-500 mt-1">•</span>
                  {point}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Issues */}
        {data.issues && data.issues.length > 0 && (
          <div>
            <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-2">
              <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              Issues Found
            </h4>
            <ul className="space-y-2">
              {data.issues.map((issue, index) => (
                <li key={index} className="text-sm text-slate-600 flex items-start gap-2">
                  <span className="text-red-500 mt-1">•</span>
                  {issue}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {data.recommendations && data.recommendations.length > 0 && (
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
            <h4 className="text-sm font-bold text-blue-800 uppercase tracking-wider mb-3 flex items-center gap-2">
              <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
              Top Recommendations
            </h4>
            <ol className="space-y-2 list-decimal list-inside text-sm text-blue-900">
              {data.recommendations.map((rec, index) => (
                <li key={index} className="pl-1">{rec}</li>
              ))}
            </ol>
          </div>
        )}

        {/* SERP Specific Data */}
        {data.serp_analysis && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-700 mb-3">SERP Analysis</h4>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-center">
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Your Words</div>
                <div className="font-bold text-slate-800">{data.serp_analysis.your_word_count}</div>
              </div>
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Avg Words</div>
                <div className="font-bold text-slate-800">{data.serp_analysis.avg_word_count}</div>
              </div>
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Predicted Rank</div>
                <div className="font-bold text-indigo-600 text-xs">{data.predicted_position}</div>
              </div>
            </div>
          </div>
        )}

        {/* Differentiation Specific Data */}
        {data.overlap_analysis && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-700 mb-3">Uniqueness Analysis</h4>
            <div className="bg-slate-50 p-3 rounded mb-3 flex justify-between items-center">
              <span className="text-sm text-slate-600">Content Similarity</span>
              <span className="font-bold text-slate-800">{data.overlap_analysis.avg_similarity}</span>
            </div>
            {data.unique_elements_found && data.unique_elements_found.length > 0 && (
              <div>
                <span className="text-xs font-bold text-slate-500 uppercase">Unique Elements:</span>
                <ul className="mt-1 space-y-1">
                  {data.unique_elements_found.map((element, index) => (
                    <li key={index} className="text-xs text-slate-600 bg-white border border-slate-200 px-2 py-1 rounded inline-block mr-2 mb-1">
                      {element}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Sentiment Analysis Data */}
        {data.tone && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-700 mb-3">Sentiment Metrics</h4>
            <div className="grid grid-cols-2 gap-2 text-center">
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Tone</div>
                <div className="font-bold text-slate-800 capitalize">{data.tone}</div>
              </div>
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Subjectivity</div>
                <div className="font-bold text-slate-800">{data.subjectivity}</div>
              </div>
            </div>
          </div>
        )}

        {/* Entity Analysis Data */}
        {data.unique_entities !== undefined && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-700 mb-3">Entity Metrics</h4>
            <div className="flex justify-between items-center bg-slate-50 p-2 rounded mb-2">
              <span className="text-xs text-slate-500">Unique Entities</span>
              <span className="font-bold text-slate-800">{data.unique_entities}</span>
            </div>
            {data.top_entities && data.top_entities.length > 0 && (
              <div>
                <span className="text-xs font-bold text-slate-500 uppercase">Top Entities:</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {data.top_entities.slice(0, 5).map((entity, idx) => (
                    <span key={idx} className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded border border-blue-100">
                      {entity.name} ({entity.count})
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Freshness Analysis Data */}
        {data.latest_year !== undefined && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-700 mb-3">Freshness Indicators</h4>
            <div className="grid grid-cols-2 gap-2 text-center">
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Latest Year</div>
                <div className="font-bold text-slate-800">{data.latest_year || 'None'}</div>
              </div>
              <div className="bg-slate-50 p-2 rounded">
                <div className="text-xs text-slate-500">Time Words</div>
                <div className="font-bold text-slate-800">{data.time_indicators}</div>
              </div>
            </div>
          </div>
        )}

        {/* Plagiarism/Originality Data */}
        {data.uniqueness !== undefined && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-700 mb-3">Originality Metrics</h4>
            <div className="bg-slate-50 p-3 rounded mb-2">
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-slate-600">Uniqueness Score</span>
                <span className="font-bold text-slate-800">{data.uniqueness}%</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div className="bg-indigo-500 h-2 rounded-full" style={{ width: `${data.uniqueness}%` }}></div>
              </div>
            </div>
            <div className="text-xs text-slate-500 text-center">
              {data.duplicate_phrases} repeated phrases detected
            </div>
          </div>
        )}
      </div>

      {/* Expandable Details */}
      {data.details && (
        <div className="mt-6 pt-4 border-t border-slate-100">
          <button 
            className="text-xs font-medium text-slate-500 hover:text-primary-600 flex items-center gap-1 transition-colors w-full justify-center"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? 'Hide Technical Details ▲' : 'Show Technical Details ▼'}
          </button>
          
          {expanded && (
            <div className="mt-4 bg-slate-50 p-4 rounded text-xs font-mono text-slate-600 overflow-x-auto border border-slate-200">
              <pre>{JSON.stringify(data.details, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ScoreCard;
