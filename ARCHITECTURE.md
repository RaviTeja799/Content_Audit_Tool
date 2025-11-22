# Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│              React 18 + Tailwind CSS Frontend                │
│                    (Port: 3000 / Vercel)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/REST API
                         │
┌────────────────────────┴────────────────────────────────────┐
│                   FLASK BACKEND API                          │
│              Python 3.11 + Flask Framework                   │
│                 (Port: 5000 / Serverless)                    │
├──────────────────────────────────────────────────────────────┤
│                    ANALYSIS MODULES                          │
├──────────────────────────────────────────────────────────────┤
│  1. SEO Analyzer          │  6. Sentiment Analyzer           │
│     - Keyword Density     │     - TextBlob Integration       │
│     - Readability (NLTK)  │     - Polarity & Subjectivity    │
│     - Headers & Meta      │     - Emotional Tone             │
│                           │                                  │
│  2. SERP Analyzer         │  7. Entity Analyzer              │
│     - Serper.dev API      │     - spaCy NLP                  │
│     - Top 10 Scraping     │     - Named Entity Recognition   │
│     - Ranking Prediction  │     - Entity Frequency           │
│                           │                                  │
│  3. AEO Analyzer          │  8. Freshness Analyzer           │
│     - Citation Detection  │     - Date References            │
│     - Structured Data     │     - Temporal Keywords          │
│     - Answer Patterns     │     - Update Indicators          │
│                           │                                  │
│  4. Humanization Analyzer │  9. Plagiarism Checker           │
│     - Sentence Variety    │     - Duplicate Detection        │
│     - Flow Analysis       │     - Originality Score          │
│     - Engagement Score    │     - Phrase Matching            │
│                           │                                  │
│  5. Differentiation       │  10. Schema Generator            │
│     - Competitor Compare  │     - JSON-LD Generation         │
│     - Uniqueness Score    │     - SEO Markup                 │
│     - Content Gap         │     - Structured Data            │
├──────────────────────────────────────────────────────────────┤
│                   AI ENHANCEMENT LAYER                       │
├──────────────────────────────────────────────────────────────┤
│  AI Suggestions Module    │  Content Comparison              │
│  - Groq API (Llama 3)     │  - Keyword Research              │
│  - Google Gemini API      │  - Side-by-side Analysis         │
│  - Improvement Tips       │  - Competitor Insights           │
├──────────────────────────────────────────────────────────────┤
│                   ENTERPRISE FEATURES                        │
├──────────────────────────────────────────────────────────────┤
│  Batch Processor          │  Share Link Manager              │
│  - Multi-URL Analysis     │  - Public Link Generation        │
│  - Progress Tracking      │  - 30-day Expiration             │
│  - Concurrent Processing  │  - Shareable Reports             │
│                           │                                  │
│  History Tracker          │  PDF Generator                   │
│  - SQLite Database        │  - ReportLab Integration         │
│  - Trend Analysis         │  - Professional Reports          │
│  - Progress Charts        │  - Client-Ready Exports          │
└──────────────────────────────────────────────────────────────┘
                         │
                         │
┌────────────────────────┴────────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
├──────────────────────────────────────────────────────────────┤
│  Serper.dev / SerpAPI     │  Google Gemini API               │
│  Groq API (Llama 3)       │  spaCy NLP Models                │
│  NLTK Corpora             │  TextBlob Sentiment              │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│  User Input │
│ (URL/Text)  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   Frontend      │
│   Validation    │
└──────┬──────────┘
       │
       ▼
┌─────────────────────┐
│  API Request        │
│  POST /api/analyze  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Text Extraction    │
│  (if URL provided)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│    Parallel Analysis (9 Modules)    │
│                                     │
│  ┌────────┐  ┌────────┐  ┌────────┐│
│  │  SEO   │  │ SERP   │  │  AEO   ││
│  └────────┘  └────────┘  └────────┘│
│                                     │
│  ┌────────┐  ┌────────┐  ┌────────┐│
│  │ Human  │  │ Differ │  │Sentiment│
│  └────────┘  └────────┘  └────────┘│
│                                     │
│  ┌────────┐  ┌────────┐  ┌────────┐│
│  │ Entity │  │Fresh   │  │Original││
│  └────────┘  └────────┘  └────────┘│
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│  Score Aggregation  │
│  Weighted Average   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  AI Enhancement     │
│  (Optional)         │
│  - Groq Suggestions │
│  - Gemini Improve   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Store in Database  │
│  (SQLite)           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  JSON Response      │
│  with Scores &      │
│  Recommendations    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Frontend           │
│  Visualization      │
│  - Charts           │
│  - Score Cards      │
│  - Insights         │
└─────────────────────┘
```

## Component Interaction

```
Frontend (React)
    │
    ├── AnalysisForm.js ──────► POST /api/analyze
    │                             │
    ├── BatchAnalyzer.js ─────► POST /api/batch-analyze
    │                             │
    ├── AISuggestions.js ─────► POST /api/ai-suggestions
    │                             │
    ├── HistoryDashboard.js ──► GET /api/history
    │                             │
    └── AdminPanel.js ─────────► POST /api/clear-data
                                  │
                                  ▼
                            Flask Backend
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    │                             │                             │
    ▼                             ▼                             ▼
Analyzers                    Utils                      External APIs
    │                             │                             │
    ├── seo_analyzer          ├── text_extractor          ├── Serper.dev
    ├── serp_analyzer         ├── serp_scraper            ├── Groq API
    ├── aeo_analyzer          ├── pdf_generator           └── Gemini API
    ├── humanization          ├── history_tracker
    ├── differentiation       ├── ai_improver
    ├── sentiment             └── share_link_manager
    ├── entity
    ├── freshness
    └── plagiarism
```

## Deployment Architecture

```
┌────────────────────────────────────────────────────────┐
│                    Vercel Platform                      │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐      ┌──────────────────┐       │
│  │   Frontend       │      │   Backend API    │       │
│  │   Static Site    │      │   Serverless     │       │
│  │   (React Build)  │◄────►│   (Python)       │       │
│  │                  │      │                  │       │
│  │  Port: 80/443    │      │  /api/* routes   │       │
│  └──────────────────┘      └──────────────────┘       │
│           │                         │                  │
│           │                         │                  │
└───────────┼─────────────────────────┼──────────────────┘
            │                         │
            │                         │
            ▼                         ▼
      ┌──────────┐            ┌──────────────┐
      │   CDN    │            │  External    │
      │  Global  │            │    APIs      │
      └──────────┘            │ - Serper.dev │
                              │ - Groq       │
                              │ - Gemini     │
                              └──────────────┘
```
