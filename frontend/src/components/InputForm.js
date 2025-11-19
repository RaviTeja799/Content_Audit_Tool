import React, { useState } from 'react';
import './InputForm.css';

function InputForm({ onAnalyze, loading }) {
  const [input, setInput] = useState('');
  const [targetKeyword, setTargetKeyword] = useState('');
  const [inputType, setInputType] = useState('text');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onAnalyze({
        input: input.trim(),
        target_keyword: targetKeyword.trim()
      });
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInput(value);
    
    // Auto-detect if URL
    if (value.startsWith('http://') || value.startsWith('https://')) {
      setInputType('url');
    } else {
      setInputType('text');
    }
  };

  return (
    <div className="input-form-container fade-in">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label htmlFor="input">
            {inputType === 'url' ? '🔗 Article URL' : '📝 Content Text'}
          </label>
          <textarea
            id="input"
            value={input}
            onChange={handleInputChange}
            placeholder="Paste your content here or enter a URL (https://example.com/article)..."
            rows={8}
            required
            disabled={loading}
          />
          <small className="input-hint">
            {inputType === 'url' 
              ? 'URL detected - will fetch and analyze content from the page'
              : 'Paste your article text or enter a URL starting with http:// or https://'
            }
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="keyword">
            🎯 Target Keyword (Optional)
          </label>
          <input
            type="text"
            id="keyword"
            value={targetKeyword}
            onChange={(e) => setTargetKeyword(e.target.value)}
            placeholder="e.g., best budget laptops 2025"
            disabled={loading}
          />
          <small className="input-hint">
            Helps analyze SERP performance and differentiation
          </small>
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={loading || !input.trim()}
        >
          {loading ? '🔄 Analyzing...' : '🚀 Analyze Content'}
        </button>
      </form>
    </div>
  );
}

export default InputForm;
