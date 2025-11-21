import React from 'react';

function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12 animate-fade-in">
      <div className="relative w-24 h-24 mb-8">
        <div className="absolute top-0 left-0 w-full h-full border-4 border-slate-100 rounded-full"></div>
        <div className="absolute top-0 left-0 w-full h-full border-4 border-primary-500 rounded-full border-t-transparent animate-spin"></div>
      </div>
      
      <h2 className="text-2xl font-bold text-slate-800 mb-2">Analyzing Your Content...</h2>
      <p className="text-slate-500 mb-8">This may take 30-60 seconds as we analyze SERP competitors</p>
      
      <div className="w-full max-w-md space-y-3">
        <div className="flex items-center text-sm text-slate-600">
          <span className="w-6 h-6 flex items-center justify-center bg-green-100 text-green-600 rounded-full mr-3">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </span>
          Extracting text & metadata
        </div>
        <div className="flex items-center text-sm text-slate-600">
          <span className="w-6 h-6 flex items-center justify-center bg-green-100 text-green-600 rounded-full mr-3">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </span>
          Analyzing SEO & Readability
        </div>
        <div className="flex items-center text-sm text-slate-600 animate-pulse">
          <span className="w-6 h-6 flex items-center justify-center bg-blue-100 text-blue-600 rounded-full mr-3">
            <svg className="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          </span>
          Fetching SERP results & Competitor Data
        </div>
        <div className="flex items-center text-sm text-slate-400">
          <span className="w-6 h-6 flex items-center justify-center bg-slate-100 text-slate-400 rounded-full mr-3">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2" fill="none" />
            </svg>
          </span>
          Comparing Differentiation & Uniqueness
        </div>
        <div className="flex items-center text-sm text-slate-400">
          <span className="w-6 h-6 flex items-center justify-center bg-slate-100 text-slate-400 rounded-full mr-3">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2" fill="none" />
            </svg>
          </span>
          Generating Actionable Recommendations
        </div>
      </div>
    </div>
  );
}

export default LoadingSpinner;
