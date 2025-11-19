import React, { useState } from 'react';
import './ScoreCard.css';

function ScoreCard({ title, icon, data, color }) {
  const [expanded, setExpanded] = useState(false);

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Work';
    return 'Poor';
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#eab308';
    if (score >= 40) return '#f97316';
    return '#ef4444';
  };

  return (
    <div className="score-card" style={{ borderTopColor: color }}>
      <div className="score-header">
        <h3>
          <span className="icon">{icon}</span>
          {title}
        </h3>
        <div className="score-badge" style={{ backgroundColor: getScoreColor(data.score) }}>
          {data.score}/100
        </div>
      </div>

      <div className="score-bar-container">
        <div 
          className="score-bar" 
          style={{ 
            width: `${data.score}%`,
            backgroundColor: getScoreColor(data.score)
          }}
        >
          <span className="score-label">{getScoreLabel(data.score)}</span>
        </div>
      </div>

      {/* Good Points */}
      {data.good_points && data.good_points.length > 0 && (
        <div className="good-points">
          <h4>✅ Strengths</h4>
          <ul>
            {data.good_points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Issues */}
      {data.issues && data.issues.length > 0 && (
        <div className="issues">
          <h4>⚠️ Issues Found</h4>
          <ul>
            {data.issues.map((issue, index) => (
              <li key={index}>{issue}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {data.recommendations && data.recommendations.length > 0 && (
        <div className="recommendations">
          <h4>💡 Top Recommendations</h4>
          <ol>
            {data.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ol>
        </div>
      )}

      {/* SERP Specific Data */}
      {data.serp_analysis && (
        <div className="serp-details">
          <h4>📊 SERP Analysis</h4>
          <div className="serp-stats">
            <div className="stat">
              <span className="stat-label">Your Word Count</span>
              <span className="stat-value">{data.serp_analysis.your_word_count}</span>
            </div>
            <div className="stat">
              <span className="stat-label">SERP Average</span>
              <span className="stat-value">{data.serp_analysis.avg_word_count}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Predicted Position</span>
              <span className="stat-value">{data.predicted_position}</span>
            </div>
          </div>
        </div>
      )}

      {/* Differentiation Specific Data */}
      {data.overlap_analysis && (
        <div className="diff-details">
          <h4>📈 Uniqueness Analysis</h4>
          <div className="diff-stats">
            <div className="stat">
              <span className="stat-label">Content Similarity</span>
              <span className="stat-value">{data.overlap_analysis.avg_similarity}</span>
            </div>
            {data.unique_elements_found && data.unique_elements_found.length > 0 && (
              <div className="unique-elements">
                <span className="stat-label">Unique Elements:</span>
                <ul>
                  {data.unique_elements_found.map((element, index) => (
                    <li key={index}>{element}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Expandable Details */}
      {data.details && (
        <button 
          className="expand-button"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? '▲ Hide Details' : '▼ Show Details'}
        </button>
      )}

      {expanded && data.details && (
        <div className="expanded-details">
          <pre>{JSON.stringify(data.details, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ScoreCard;
