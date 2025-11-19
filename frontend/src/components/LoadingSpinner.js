import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <h2>Analyzing Your Content...</h2>
      <p>This may take 30-60 seconds as we analyze SERP competitors</p>
      <div className="loading-steps">
        <div className="step">✓ Extracting text</div>
        <div className="step">✓ Analyzing SEO metrics</div>
        <div className="step">⏳ Fetching SERP results</div>
        <div className="step">⏳ Comparing with competitors</div>
        <div className="step">⏳ Generating recommendations</div>
      </div>
    </div>
  );
}

export default LoadingSpinner;
