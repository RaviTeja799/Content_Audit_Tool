import React, { useState } from 'react';
import axios from 'axios';
import InputForm from './components/InputForm';
import ResultsDashboard from './components/ResultsDashboard';
import LoadingSpinner from './components/LoadingSpinner';
import KeywordResearch from './components/KeywordResearch';
import ContentComparison from './components/ContentComparison';
import HistoryDashboard from './components/HistoryDashboard';
import BatchAnalyzer from './components/BatchAnalyzer';
import AISuggestions from './components/AISuggestions';
import SchemaMarkup from './components/SchemaMarkup';
import AdminPanel from './components/AdminPanel';
import './App.css';

// Use environment variable or fallback to relative path for Vercel
const API_URL = process.env.REACT_APP_API_URL || '/api';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentInput, setCurrentInput] = useState({ input: '', target_keyword: '' });
  const [activeTab, setActiveTab] = useState('analysis'); // analysis, history, batch, admin

  const handleAnalyze = async (inputData) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setCurrentInput(inputData);

    try {
      const response = await axios.post(`${API_URL}/api/analyze`, inputData, {
        timeout: 60000, // 60 second timeout
      });
      setResults(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'Failed to analyze content. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl mb-4">
            Content Quality Audit Tool
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Analyze your content across 5 key dimensions: SEO, SERP Performance, AEO, Humanization & Differentiation
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex flex-wrap justify-center mb-8 border-b border-slate-200">
          <button
            onClick={() => setActiveTab('analysis')}
            className={`px-4 sm:px-6 py-2 sm:py-3 text-sm sm:text-base font-medium transition-all ${
              activeTab === 'analysis'
                ? 'border-b-2 border-purple-600 text-purple-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Content Analysis
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-4 sm:px-6 py-2 sm:py-3 text-sm sm:text-base font-medium transition-all ${
              activeTab === 'history'
                ? 'border-b-2 border-purple-600 text-purple-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            History & Progress
          </button>
          <button
            onClick={() => setActiveTab('batch')}
            className={`px-4 sm:px-6 py-2 sm:py-3 text-sm sm:text-base font-medium transition-all ${
              activeTab === 'batch'
                ? 'border-b-2 border-purple-600 text-purple-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Batch Analyzer
          </button>
          <button
            onClick={() => setActiveTab('admin')}
            className={`px-4 sm:px-6 py-2 sm:py-3 text-sm sm:text-base font-medium transition-all ${
              activeTab === 'admin'
                ? 'border-b-2 border-purple-600 text-purple-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Admin
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'analysis' && (
          <>
            <InputForm onAnalyze={handleAnalyze} loading={loading} />

            {loading && <LoadingSpinner />}

            {error && (
              <div className="mt-8 bg-red-50 border-l-4 border-red-500 p-4 rounded-md shadow-sm max-w-4xl mx-auto">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Analysis Error</h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {results && !loading && <ResultsDashboard results={results} />}

            {/* Additional Features - Show after analysis */}
            {results && !loading && (
              <div className="mt-8 space-y-8">
                {results.schema && <SchemaMarkup schema={results.schema} />}
                <KeywordResearch targetKeyword={currentInput.target_keyword} />
                <ContentComparison 
                  content={currentInput.input} 
                  keyword={currentInput.target_keyword}
                  metadata={{
                    word_count: results.word_count,
                    headers: results.seo?.headers || [],
                    has_images: false,
                    has_videos: false,
                    has_lists: false,
                    has_tables: false,
                    text: currentInput.input
                  }}
                />
                <AISuggestions 
                  content={currentInput.input}
                  analysisResults={results}
                />
              </div>
            )}
          </>
        )}

        {activeTab === 'history' && <HistoryDashboard />}

        {activeTab === 'batch' && <BatchAnalyzer />}

        {activeTab === 'admin' && <AdminPanel />}
      </div>

      <footer className="mt-20 border-t border-slate-200 py-8 text-center text-slate-500 text-sm">
        <p>Built for BEASTBOYZ PROJECT | Powered by AI Analysis</p>
      </footer>
    </div>
  );
}

export default App;
