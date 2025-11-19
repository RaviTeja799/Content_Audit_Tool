import React from 'react';
import ScoreCard from './ScoreCard';
import './ResultsDashboard.css';

function ResultsDashboard({ results }) {
  const getScoreColor = (score) => {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#eab308';
    if (score >= 40) return '#f97316';
    return '#ef4444';
  };

  return (
    <div className="results-dashboard fade-in">
      {/* Overall Summary */}
      <div className="overall-summary">
        <h2>📊 Overall Content Quality</h2>
        <div className="overall-score-circle">
          <svg width="180" height="180" viewBox="0 0 180 180">
            <circle
              cx="90"
              cy="90"
              r="80"
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="12"
            />
            <circle
              cx="90"
              cy="90"
              r="80"
              fill="none"
              stroke={getScoreColor(results.overall_score)}
              strokeWidth="12"
              strokeDasharray={`${results.overall_score * 5.03} 503`}
              strokeLinecap="round"
              transform="rotate(-90 90 90)"
            />
          </svg>
          <div className="score-text">
            <span className="score-number">{results.overall_score}</span>
            <span className="score-label">/100</span>
          </div>
        </div>
        <div className="meta-info">
          <p><strong>Word Count:</strong> {results.word_count}</p>
          {results.target_keyword && (
            <p><strong>Target Keyword:</strong> {results.target_keyword}</p>
          )}
          {results.url && (
            <p><strong>URL:</strong> <a href={results.url} target="_blank" rel="noopener noreferrer">{results.url}</a></p>
          )}
        </div>
      </div>

      {/* Individual Scores */}
      <div className="scores-grid">
        <ScoreCard
          title="SEO Score"
          icon="🔍"
          data={results.seo}
          color="#3b82f6"
        />
        <ScoreCard
          title="SERP Performance"
          icon="📈"
          data={results.serp_performance}
          color="#8b5cf6"
        />
        <ScoreCard
          title="AEO Score"
          icon="🤖"
          data={results.aeo}
          color="#10b981"
        />
        <ScoreCard
          title="Humanization"
          icon="👤"
          data={results.humanization}
          color="#f59e0b"
        />
        <ScoreCard
          title="Differentiation"
          icon="⭐"
          data={results.differentiation}
          color="#ec4899"
        />
      </div>
    </div>
  );
}

export default ResultsDashboard;
