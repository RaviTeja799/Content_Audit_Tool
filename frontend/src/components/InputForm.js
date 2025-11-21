import React, { useState } from 'react';

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
    <div className="bg-white rounded-xl shadow-lg p-4 sm:p-8 mb-8 max-w-4xl mx-auto border border-slate-100">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="input" className="block text-sm font-semibold text-slate-700 mb-2">
            {inputType === 'url' ? 'Article URL' : 'Content Text'}
          </label>
          <div className="relative rounded-md shadow-sm">
            <textarea
              id="input"
              value={input}
              onChange={handleInputChange}
              placeholder="Paste your content here or enter a URL (https://example.com/article)..."
              rows={8}
              required
              disabled={loading}
              className="block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm p-4 border"
            />
          </div>
          <p className="mt-2 text-sm text-slate-500">
            {inputType === 'url' 
              ? 'URL detected - will fetch and analyze content from the page'
              : 'Paste your article text or enter a URL starting with http:// or https://'
            }
          </p>
        </div>

        <div>
          <label htmlFor="keyword" className="block text-sm font-semibold text-slate-700 mb-2">
            Target Keyword (Optional)
          </label>
          <input
            type="text"
            id="keyword"
            value={targetKeyword}
            onChange={(e) => setTargetKeyword(e.target.value)}
            placeholder="e.g., best budget laptops 2025"
            disabled={loading}
            className="block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm p-3 border"
          />
          <p className="mt-2 text-sm text-slate-500">
            Helps analyze SERP performance and differentiation
          </p>
        </div>

        <div className="pt-4">
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className={`w-full flex justify-center py-4 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200 ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing Content...
              </span>
            ) : 'Analyze Content'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default InputForm;
