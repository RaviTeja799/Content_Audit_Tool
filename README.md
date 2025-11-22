# Content Quality Audit Tool - AI-Powered Content Analysis Platform

> **Built for Evolutyz Buildathon 2025 - Track 1: Technical Teams**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

---

## Video Demo

**Watch the complete demo here:** [Demo Video Link](#) *(Upload your 2-4 minute demo video and add link)*

The video demonstrates:
- Problem statement and real-world use case
- Complete workflow of the AI-powered analysis
- All 9 analysis modules in action
- Enterprise features (batch processing, AI suggestions, PDF reports)
- Final output and results visualization

---

## A. Problem Statement

### The Challenge
Content creators, SEO specialists, and digital marketers face several critical challenges:

1. **Lack of Comprehensive Analysis**: Existing tools analyze content in isolation (only SEO or only readability), missing the complete picture
2. **Time-Consuming Manual Audits**: Manually checking content against top competitors takes hours
3. **No AI-Powered Insights**: Traditional tools provide scores but no actionable improvement suggestions
4. **Expensive Enterprise Tools**: Professional-grade content analysis tools cost $100-500/month
5. **No Historical Tracking**: Creators can't track content quality improvements over time
6. **Fragmented Workflow**: Need to use multiple tools for SEO, sentiment, readability, and competitor analysis

### Real-World Impact
- **75% of marketers** struggle to measure content quality objectively
- **Average time per content audit**: 2-3 hours manually
- **Cost of enterprise tools**: $2,000-6,000 annually per user

---

## B. Solution Overview

### Our Approach
An **AI-powered, comprehensive content analysis platform** that combines **9+ analysis dimensions** into a single unified dashboard with enterprise features.

### Key Innovation
- **Multi-Dimensional Analysis**: SEO, SERP, AEO, Humanization, Sentiment, Entity Recognition, Freshness, Originality, and Differentiation
- **AI-Powered Suggestions**: Uses Groq (Llama 3) and Google Gemini to provide personalized improvement recommendations
- **Automated Competitor Analysis**: Automatically scrapes and compares content with top 10 SERP results
- **Real-Time Processing**: Instant analysis with progress tracking for batch operations
- **Historical Intelligence**: Track content improvements over time with trend visualization

### Expected Impact
- **Reduce audit time** from 2-3 hours to 30 seconds
- **Save $2,000+/year** per user compared to enterprise tools
- **Improve content quality** by 40-60% with AI suggestions
- **Increase search rankings** through data-driven optimization
- **Enable batch processing** for agencies managing 100+ client sites

### Value Proposition
- **For Content Creators**: Optimize blog posts before publishing, track quality improvements
- **For SEO Specialists**: Batch process client content, generate professional audit reports
- **For Agencies**: Scale content audits, share reports with stakeholders
- **For Businesses**: Maintain content quality standards across teams

---

## C. Architecture Diagram

### System Architecture

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

### Data Flow

```
User Input (URL/Text) 
    ↓
Frontend Validation
    ↓
API Request (/api/analyze)
    ↓
Text Extraction (if URL)
    ↓
Parallel Analysis (9 modules)
    ↓
Score Aggregation
    ↓
AI Enhancement (optional)
    ↓
Result Storage (SQLite)
    ↓
Response with Scores & Insights
    ↓
Frontend Visualization
```

---

## D. Tech Stack

### Backend Technologies
```yaml
Language: Python 3.11+
Framework: Flask 3.0.0
AI/ML Libraries:
  - Groq 0.4.1 (Llama 3 integration)
  - Google Gemini API (AI improvements)
  - spaCy 3.7.2 (Entity recognition)
  - NLTK 3.8.1 (NLP processing)
  - TextBlob 0.17.1 (Sentiment analysis)
  - scikit-learn 1.3.2 (Text comparison)

Analysis Tools:
  - BeautifulSoup4 4.12.2 (Web scraping)
  - Requests 2.31.0 (HTTP client)
  - textstat 0.7.3 (Readability metrics)
  - ReportLab 4.0.7 (PDF generation)

Database: SQLite3 (built-in)
Environment: python-dotenv 1.0.0
```

### Frontend Technologies
```yaml
Framework: React 18.2.0
UI Library: Tailwind CSS 3.4.1
Charts: Recharts 2.15.4
HTTP Client: Axios 1.6.2
Build Tool: Create React App 5.0.1
Additional:
  - PostCSS 8.4.31
  - Autoprefixer 10.4.16
```

### APIs & External Services
```yaml
SERP Data:
  - Serper.dev API (Primary)
  - SerpAPI (Alternative)
AI Services:
  - Groq (Llama 3) - Suggestions
  - Google Gemini - Improvements
NLP Models:
  - spaCy en_core_web_sm
  - NLTK punkt, stopwords
  - TextBlob corpora
```

### Deployment
```yaml
Frontend: Vercel / Netlify
Backend: Vercel Serverless / Railway / Render
Version Control: Git / GitHub
CI/CD: GitHub Actions (optional)
```

---

## E. How to Run Your Project

### Prerequisites Installation

**1. Install Python 3.11+**
```bash
# Download from https://www.python.org/downloads/
python --version  # Verify installation
```

**2. Install Node.js 16+**
```bash
# Download from https://nodejs.org/
node --version  # Verify installation
npm --version   # Verify npm installation
```

**3. Clone the Repository**
```bash
git clone https://github.com/RaviTeja799/Content_Audit_Tool.git
cd Content_Audit_Tool
```

---

### Backend Setup (Flask API)

**Step 1: Navigate to Backend Directory**
```bash
cd backend
```

**Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Download NLP Data**
```bash
# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"

# Download TextBlob corpora
python -m textblob.download_corpora

# Download spaCy model
python -m spacy download en_core_web_sm
```

**Step 5: Configure Environment Variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API keys
notepad .env  # Windows
nano .env     # macOS/Linux
```

Add the following keys:
```env
# SERP API (Choose one)
SERPER_API_KEY=your_serper_api_key_here
# OR
SERPAPI_KEY=your_serpapi_key_here

# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**Step 6: Start Backend Server**
```bash
python app.py
```

Backend will run at: `http://localhost:5000`

---

### Frontend Setup (React App)

**Step 1: Open New Terminal**
```bash
# Navigate to frontend directory
cd frontend
```

**Step 2: Install Dependencies**
```bash
npm install
```

**Step 3: Start Development Server**
```bash
npm start
```

Frontend will run at: `http://localhost:3000`

---

### Quick Start (Windows Users)

We've included batch scripts for easy setup:

```bash
# Run automated setup
setup.bat

# Start backend (Terminal 1)
start-backend.bat

# Start frontend (Terminal 2)
start-frontend.bat
```

---

### Vercel Deployment (Production)

**Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

**Step 2: Login to Vercel**
```bash
vercel login
```

**Step 3: Deploy**
```bash
vercel
```

**Step 4: Add Environment Variables in Vercel Dashboard**
- Go to Project Settings → Environment Variables
- Add all API keys from .env file

**Step 5: Deploy to Production**
```bash
vercel --prod
```

See `VERCEL_DEPLOYMENT.md` for detailed deployment instructions.

---

## F. API Keys / Usage Notes

### Required API Keys

#### 1. Serper.dev API (Recommended)
- **Purpose**: SERP data for competitor analysis
- **Free Tier**: 2,500 searches/month
- **Sign Up**: [https://serper.dev/](https://serper.dev/)
- **Cost**: $5 per 1,000 searches after free tier
- **Setup**:
  1. Sign up with Google OAuth
  2. Navigate to API Keys section
  3. Copy API key
  4. Add to `.env` as `SERPER_API_KEY`

#### 2. Groq API (AI Suggestions)
- **Purpose**: Generate AI-powered improvement suggestions
- **Free Tier**: Generous free tier (currently)
- **Sign Up**: [https://console.groq.com/](https://console.groq.com/)
- **Model Used**: Llama 3 70B
- **Setup**:
  1. Create account at console.groq.com
  2. Navigate to API Keys
  3. Create new key
  4. Add to `.env` as `GROQ_API_KEY`

#### 3. Google Gemini API (AI Improvements)
- **Purpose**: Advanced content improvement recommendations
- **Free Tier**: 60 requests/minute
- **Sign Up**: [https://ai.google.dev/](https://ai.google.dev/)
- **Model Used**: Gemini 1.5 Flash
- **Setup**:
  1. Go to Google AI Studio
  2. Get API Key
  3. Add to `.env` as `GEMINI_API_KEY`

### Alternative: SerpAPI
- **If Serper.dev is unavailable**:
  - Sign up at [https://serpapi.com/](https://serpapi.com/)
  - Free tier: 100 searches/month
  - Add to `.env` as `SERPAPI_KEY`

### Important Security Notes

**DO NOT:**
- Commit `.env` file to Git
- Share API keys publicly
- Hardcode keys in source code
- Push credentials to GitHub

**ALWAYS:**
- Use `.env.example` as template
- Add `.env` to `.gitignore`
- Use environment variables
- Rotate keys if exposed

### Environment File Template

```env
# .env.example (This file is safe to commit)

# SERP API (Choose one)
SERPER_API_KEY=your_serper_api_key_here
# OR
SERPAPI_KEY=your_serpapi_key_here

# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Rate Limits & Costs

| Service | Free Tier | Rate Limit | Cost After Free |
|---------|-----------|------------|-----------------|
| Serper.dev | 2,500/month | - | $5/1,000 searches |
| Groq | Generous | ~30 req/min | Currently free |
| Gemini | 60/min | 60 req/min | Free tier available |

---

## G. Sample Inputs & Outputs

### Sample Input 1: URL Analysis

**Input:**
```json
{
  "url": "https://example.com/blog/artificial-intelligence-guide",
  "keyword": "artificial intelligence",
  "mode": "url"
}
```

**API Endpoint:** `POST /api/analyze`

**Output:**
```json
{
  "overall_score": 85.4,
  "content_length": 2847,
  "analysis": {
    "seo": {
      "score": 88,
      "keyword_density": 2.3,
      "readability": {
        "flesch_reading_ease": 68.5,
        "grade_level": "10-12"
      },
      "headers_count": 12,
      "recommendations": [
        "Add more H2 subheadings",
        "Optimize meta description length"
      ]
    },
    "serp": {
      "score": 82,
      "predicted_position": 3,
      "top_competitors": [
        {
          "url": "competitor1.com",
          "similarity": 0.75,
          "ranking": 1
        }
      ]
    },
    "humanization": {
      "score": 91,
      "sentence_variety": 0.85,
      "flow_score": 0.88,
      "engagement": "high"
    },
    "sentiment": {
      "polarity": 0.15,
      "subjectivity": 0.42,
      "tone": "neutral-positive"
    },
    "entities": {
      "persons": ["Elon Musk", "Geoffrey Hinton"],
      "organizations": ["OpenAI", "Google"],
      "technologies": ["GPT-4", "Neural Networks"]
    },
    "freshness": {
      "score": 78,
      "recent_references": 5,
      "update_indicators": 2
    },
    "originality": {
      "score": 94,
      "unique_content_ratio": 0.94,
      "duplicate_phrases": 6
    }
  },
  "ai_suggestions": [
    "Add more recent examples from 2025",
    "Include practical use cases",
    "Improve technical depth in section 3"
  ]
}
```

### Sample Input 2: Text Analysis

**Input:**
```json
{
  "text": "Artificial intelligence is transforming how businesses operate. Machine learning algorithms analyze vast amounts of data to uncover patterns and insights. This technology enables automation, predictive analytics, and intelligent decision-making across industries.",
  "keyword": "artificial intelligence",
  "mode": "text"
}
```

**Output:**
```json
{
  "overall_score": 72.5,
  "content_length": 247,
  "analysis": {
    "seo": {
      "score": 75,
      "keyword_density": 1.6,
      "readability": {
        "flesch_reading_ease": 52.3,
        "grade_level": "College"
      }
    },
    "humanization": {
      "score": 68,
      "sentence_variety": 0.72,
      "flow_score": 0.75
    },
    "sentiment": {
      "polarity": 0.25,
      "subjectivity": 0.35,
      "tone": "positive-informative"
    }
  },
  "recommendations": [
    "Content too short - aim for 1000+ words",
    "Add more examples and use cases",
    "Include statistics or data points"
  ]
}
```

### Sample Input 3: Batch Analysis

**Input:**
```json
{
  "urls": [
    "https://example1.com/article1",
    "https://example2.com/article2",
    "https://example3.com/article3"
  ],
  "keyword": "content marketing"
}
```

**API Endpoint:** `POST /api/batch-analyze`

**Output:**
```json
{
  "batch_id": "batch_20250122_abc123",
  "total_urls": 3,
  "results": [
    {
      "url": "https://example1.com/article1",
      "status": "completed",
      "overall_score": 88.5,
      "analysis_time": "12.3s"
    },
    {
      "url": "https://example2.com/article2",
      "status": "completed",
      "overall_score": 76.2,
      "analysis_time": "10.8s"
    },
    {
      "url": "https://example3.com/article3",
      "status": "completed",
      "overall_score": 92.1,
      "analysis_time": "11.5s"
    }
  ],
  "average_score": 85.6,
  "total_time": "34.6s"
}
```

### Sample Output: PDF Report

Generated PDF includes:
- Executive Summary with overall score
- Detailed breakdown of all 9 analysis dimensions
- Visual charts and graphs
- Competitor comparison table
- AI-powered recommendations
- Action items checklist

**PDF Generation Endpoint:** `POST /api/export-pdf`

### Sample Output: AI Suggestions

**Input:** Content with score 65/100

**AI-Generated Suggestions:**
```json
{
  "suggestions": [
    {
      "category": "SEO",
      "priority": "high",
      "recommendation": "Increase keyword density to 1.5-2.5% by adding 'artificial intelligence' in subheadings"
    },
    {
      "category": "Content Quality",
      "priority": "high",
      "recommendation": "Expand content to 1500+ words. Current length (687 words) is below optimal range for ranking."
    },
    {
      "category": "Engagement",
      "priority": "medium",
      "recommendation": "Add bullet points, numbered lists, and visual breaks to improve scanability"
    },
    {
      "category": "Freshness",
      "priority": "medium",
      "recommendation": "Include recent data from 2024-2025. Add publication date and 'last updated' timestamp."
    }
  ]
}
```

---

## H. Video Demo Link

**Complete Project Demonstration**

**Video URL:** [Add your video link here]

**Platforms accepted:**
- YouTube (unlisted)
- Loom
- Google Drive
- Streamlit Cloud

**Video must cover:**
1. Problem statement (30 seconds)
2. Solution overview (30 seconds)
3. Live demo of key features (2 minutes)
   - Single URL analysis
   - Batch processing
   - AI suggestions
   - PDF export
   - History tracking
4. Results and impact (30 seconds)
5. Q&A or future roadmap (30 seconds)

**Recording tips:**
- Use screen recording software (OBS, Loom, Zoom)
- Show real analysis results
- Demonstrate enterprise features
- Keep under 4 minutes
- Add subtitles if possible

---

## Project Structure

```
Content_Audit_Tool/
├── api/
│   └── index.py                    # Vercel serverless entry point
├── backend/
│   ├── analyzers/                  # 10 analysis modules
│   │   ├── seo_analyzer.py
│   │   ├── serp_analyzer.py
│   │   ├── aeo_analyzer.py
│   │   ├── humanization_analyzer.py
│   │   ├── differentiation_analyzer.py
│   │   ├── sentiment_analyzer.py
│   │   ├── entity_analyzer.py
│   │   ├── freshness_analyzer.py
│   │   ├── plagiarism_checker.py
│   │   ├── schema_generator.py
│   │   └── keyword_researcher.py
│   ├── utils/                      # Utility modules
│   │   ├── text_extractor.py
│   │   ├── serp_scraper.py
│   │   ├── pdf_generator.py
│   │   ├── history_tracker.py
│   │   ├── ai_improver.py
│   │   └── share_link_manager.py
│   ├── app.py                      # Main Flask application
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── ScoreCard.js
│   │   │   ├── AnalysisForm.js
│   │   │   ├── BatchAnalyzer.js
│   │   │   ├── HistoryDashboard.js
│   │   │   ├── AISuggestions.js
│   │   │   ├── ContentComparison.js
│   │   │   ├── KeywordResearch.js
│   │   │   ├── SchemaMarkup.js
│   │   │   └── AdminPanel.js
│   │   ├── App.js                  # Main React app
│   │   └── index.js                # Entry point
│   ├── public/
│   ├── package.json                # npm dependencies
│   └── tailwind.config.js          # Tailwind configuration
├── vercel.json                     # Vercel deployment config
├── VERCEL_DEPLOYMENT.md            # Deployment guide
├── README.md                       # This file
├── CONTRIBUTING.md                 # Contribution guidelines
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_INFO.md                 # Detailed project info
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore rules
```

---

## API Endpoints

### Analysis Endpoints
- `POST /api/analyze` - Single content analysis
- `POST /api/batch-analyze` - Multiple URL analysis
- `POST /api/batch-status/<batch_id>` - Check batch progress

### AI Enhancement
- `POST /api/ai-suggestions` - Get AI improvement suggestions
- `POST /api/keyword-research` - Research related keywords
- `POST /api/content-comparison` - Compare with competitors
- `POST /api/schema-markup` - Generate structured data

### Export & Share
- `POST /api/export-pdf` - Generate PDF report
- `POST /api/share-link` - Create shareable link
- `GET /api/share/<share_id>` - Access shared report

### History & Management
- `GET /api/history` - Get analysis history
- `GET /api/history/<analysis_id>` - Get specific analysis
- `DELETE /api/history/<analysis_id>` - Delete analysis
- `POST /api/clear-data` - Clear all data

---

## Features Showcase

### 1. Comprehensive Analysis Dashboard
![Dashboard Screenshot](add-screenshot-here)

### 2. Batch Processing Interface
![Batch Analysis Screenshot](add-screenshot-here)

### 3. AI-Powered Suggestions
![AI Suggestions Screenshot](add-screenshot-here)

### 4. Historical Tracking
![History Dashboard Screenshot](add-screenshot-here)

---

## Performance Metrics

- **Analysis Speed**: 10-30 seconds per article
- **Batch Processing**: Up to 100 URLs concurrently
- **Accuracy**: Based on industry-standard NLP libraries
- **API Response Time**: < 2 seconds (excluding external API calls)
- **Database**: SQLite (unlimited local storage)

---

## Future Enhancements

- [ ] Multi-language support (Spanish, French, German)
- [ ] WordPress plugin integration
- [ ] Chrome extension for on-page analysis
- [ ] Team collaboration features
- [ ] Custom scoring weights
- [ ] Export to Excel/CSV
- [ ] Dark mode UI
- [ ] API authentication and rate limiting
- [ ] Advanced analytics dashboard
- [ ] Integration with Google Search Console

---

## Team & Contributors

**Developed for Evolutyz Buildathon 2025**

**Team BEASTBOYZ PROJECT**

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2025 BEASTBOYZ PROJECT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Acknowledgments

- **NLTK Team** - Natural Language Processing
- **spaCy** - Industrial-strength NLP
- **Groq** - Lightning-fast AI inference
- **Google** - Gemini AI API
- **Serper.dev** - SERP API service
- **Flask** - Web framework
- **React** - UI library
- **Tailwind CSS** - Styling framework

---

## Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/RaviTeja799/Content_Audit_Tool/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/RaviTeja799/Content_Audit_Tool/discussions)
- **Documentation**: See [QUICKSTART.md](QUICKSTART.md) and [PROJECT_INFO.md](PROJECT_INFO.md)

---

## Buildathon Submission Checklist

- [x] Source code organized in folders
- [x] requirements.txt included
- [x] .env.example with placeholder keys
- [x] README.md with all required sections
- [x] Architecture diagram included
- [x] Complete tech stack documented
- [x] Step-by-step run instructions
- [x] Sample inputs & outputs provided
- [ ] Demo video uploaded and linked
- [x] No sensitive API keys in code
- [x] Code properly commented
- [x] Git repository structured

---

**Built for BEASTBOYZ PROJECT** | **Powered by AI Analysis** | **Evolutyz Buildathon 2025**
