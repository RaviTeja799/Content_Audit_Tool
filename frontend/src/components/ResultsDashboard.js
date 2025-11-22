import React, { useState } from 'react';
import ScoreCard from './ScoreCard';
import axios from 'axios';
import { API_URL } from '../config/api';

function ResultsDashboard({ results }) {
  const [isExporting, setIsExporting] = useState(false);

  const getScoreColor = (score) => {
    if (score >= 80) return '#22c55e';
    if (score >= 60) return '#eab308';
    if (score >= 40) return '#f97316';
    return '#ef4444';
  };

  const handleExportPDF = async () => {
    try {
      setIsExporting(true);
      
      const response = await axios.post(
        `${API_URL}/api/export-pdf`,
        results,
        {
          responseType: 'blob',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      // Create download link
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Generate filename with timestamp
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
      link.download = `content-audit-${timestamp}.pdf`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error exporting PDF:', error);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="space-y-12 animate-fade-in">
      {/* Overall Summary */}
      <div className="bg-white rounded-xl shadow-lg p-4 sm:p-8 border border-slate-100">
        <div className="flex justify-between items-start mb-8">
          <h2 className="text-2xl font-bold text-slate-800">Overall Content Quality</h2>
          
          {/* Export PDF Button */}
          <button
            onClick={handleExportPDF}
            disabled={isExporting}
            className={`
              px-6 py-2.5 rounded-lg font-medium transition-all duration-200
              ${isExporting 
                ? 'bg-slate-300 text-slate-500 cursor-not-allowed' 
                : 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-md active:scale-95'
              }
            `}
          >
            {isExporting ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Generating...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Export PDF
              </span>
            )}
          </button>
        </div>
        
        <div className="flex flex-col md:flex-row items-center justify-center gap-12">
          <div className="relative w-48 h-48 flex-shrink-0">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 180 180">
              <circle
                cx="90"
                cy="90"
                r="80"
                fill="none"
                stroke="#f1f5f9"
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
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold text-slate-800">{results.overall_score}</span>
              <span className="text-slate-400 text-lg font-medium">/100</span>
            </div>
          </div>

          <div className="flex-1 space-y-4 w-full max-w-md">
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-100 flex justify-between items-center">
              <span className="text-slate-600 font-medium">Word Count</span>
              <span className="text-slate-900 font-bold">{results.word_count.toLocaleString()} words</span>
            </div>
            
            {results.target_keyword && (
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-100 flex justify-between items-center">
                <span className="text-slate-600 font-medium">Target Keyword</span>
                <span className="text-slate-900 font-bold">{results.target_keyword}</span>
              </div>
            )}
            
            {results.url && (
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-100 flex flex-col">
                <span className="text-slate-600 font-medium mb-1">Source URL</span>
                <a 
                  href={results.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-primary-600 hover:text-primary-700 truncate font-medium"
                >
                  {results.url}
                </a>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Individual Scores */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ScoreCard
          title="SEO Score"
          data={results.seo}
          color="blue"
        />
        <ScoreCard
          title="SERP Performance"
          data={results.serp_performance}
          color="indigo"
        />
        <ScoreCard
          title="AEO Score"
          data={results.aeo}
          color="emerald"
        />
        <ScoreCard
          title="Humanization"
          data={results.humanization}
          color="amber"
        />
        {results.sentiment && (
          <ScoreCard
            title="Sentiment Analysis"
            data={results.sentiment}
            color="purple"
          />
        )}
        {results.entities && (
          <ScoreCard
            title="Entity Recognition"
            data={results.entities}
            color="cyan"
          />
        )}
        {results.freshness && (
          <ScoreCard
            title="Content Freshness"
            data={results.freshness}
            color="green"
          />
        )}
        {results.plagiarism && (
          <ScoreCard
            title="Originality Check"
            data={results.plagiarism}
            color="rose"
          />
        )}
        <div className="lg:col-span-2">
          <ScoreCard
            title="Differentiation"
            data={results.differentiation}
            color="pink"
          />
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
