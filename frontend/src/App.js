import React, { useState } from 'react';
import axios from 'axios';
import InputForm from './components/InputForm';
import ResultsDashboard from './components/ResultsDashboard';
import LoadingSpinner from './components/LoadingSpinner';
import './App.css';

const API_URL = 'http://localhost:5000';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (inputData) => {
    setLoading(true);
    setError(null);
    setResults(null);

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
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🎯 Content Quality Audit Tool</h1>
          <p className="subtitle">
            Analyze your content across 5 key dimensions: SEO, SERP Performance, AEO, Humanization & Differentiation
          </p>
        </header>

        <InputForm onAnalyze={handleAnalyze} loading={loading} />

        {loading && <LoadingSpinner />}

        {error && (
          <div className="error-box">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {results && !loading && <ResultsDashboard results={results} />}
      </div>

      <footer className="footer">
        <p>Built for BEASTBOYZ PROJECT | Powered by AI Analysis</p>
      </footer>
    </div>
  );
}

export default App;
