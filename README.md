# Content Quality Audit Tool

A Comprehensive AI-Powered Content Analysis Platform

Analyze your content across 9+ dimensions with enterprise-grade features including batch processing, PDF reports, and AI-powered improvement suggestions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

---

## Features

### Core Analysis Modules
- **SEO Analysis** - Keyword density, readability, headers, meta tags optimization
- **SERP Performance** - Compare against top 10 search results, predict ranking position
- **AEO (Answer Engine Optimization)** - Citations, structured data, AI-friendly patterns
- **Humanization Score** - Natural language flow, sentence variety, engagement metrics
- **Content Differentiation** - Uniqueness analysis vs top competitors
- **Sentiment Analysis** - Emotional tone, subjectivity, polarity detection
- **Entity Recognition** - Named entity extraction and frequency analysis
- **Content Freshness** - Temporal relevance, date references, update indicators
- **Originality Check** - Plagiarism detection, duplicate phrase identification

### Enterprise Features
- **Batch Analysis** - Process multiple URLs simultaneously with progress tracking
- **History & Progress** - Track improvements over time with interactive charts
- **PDF Export** - Generate professional audit reports
- **Share Links** - Create public shareable links with expiration
- **AI Suggestions** - Get personalized improvement recommendations
- **Content Comparison** - Side-by-side analysis with #1 ranking competitor
- **Keyword Research** - Discover related keywords and search volumes
- **Schema Markup** - Auto-generate structured data for SEO

---

## Tech Stack

### Backend
- **Framework**: Flask (Python 3.11+)
- **AI/ML**: Groq (Llama 3), Google Gemini
- **Analysis**: NLTK, TextBlob, spaCy, scikit-learn
- **Web Scraping**: BeautifulSoup4, Requests
- **Database**: SQLite
- **PDF Generation**: ReportLab

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Build Tool**: Create React App

---

## Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher
- **API Keys** (Required for full functionality):
  - [Serper.dev](https://serper.dev/) or [SerpAPI](https://serpapi.com/) - SERP data
  - [Groq](https://console.groq.com/) - AI suggestions
  - [Google Gemini](https://ai.google.dev/) - AI improvements

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Content_Audit_Tool.git
cd Content_Audit_Tool
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"

# Install TextBlob corpora
python -m textblob.download_corpora

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys

# Start the backend server
python app.py
```

The backend will run at `http://localhost:5000`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will run at `http://localhost:3000`

---

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# SERP API (Choose one)
SERPER_API_KEY=your_serper_api_key
# OR
SERPAPI_KEY=your_serpapi_key

# AI API Keys
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

### Getting API Keys

1. **Serper.dev**: Sign up at [serper.dev](https://serper.dev/) (Free tier: 2,500 searches)
2. **Groq**: Create account at [console.groq.com](https://console.groq.com/) (Free tier available)
3. **Google Gemini**: Get API key from [ai.google.dev](https://ai.google.dev/)

---

## Project Structure

```
Content_Audit_Tool/
├── backend/
│   ├── analyzers/           # Analysis modules
│   │   ├── seo_analyzer.py
│   │   ├── serp_analyzer.py
│   │   ├── aeo_analyzer.py
│   │   ├── humanization_analyzer.py
│   │   ├── differentiation_analyzer.py
│   │   ├── sentiment_analyzer.py
│   │   ├── entity_analyzer.py
│   │   ├── freshness_analyzer.py
│   │   ├── plagiarism_checker.py
│   │   ├── keyword_researcher.py
│   │   ├── content_comparator.py
│   │   └── schema_generator.py
│   ├── utils/               # Utility functions
│   │   ├── text_extractor.py
│   │   ├── serp_scraper.py
│   │   ├── pdf_generator.py
│   │   ├── history_tracker.py
│   │   ├── ai_improver.py
│   │   └── share_link_manager.py
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── InputForm.js
│   │   │   ├── ResultsDashboard.js
│   │   │   ├── ScoreCard.js
│   │   │   ├── HistoryDashboard.js
│   │   │   ├── BatchAnalyzer.js
│   │   │   ├── AISuggestions.js
│   │   │   ├── ContentComparison.js
│   │   │   ├── KeywordResearch.js
│   │   │   ├── SchemaMarkup.js
│   │   │   └── AdminPanel.js
│   │   ├── App.js          # Main application
│   │   └── index.js        # Entry point
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   └── tailwind.config.js  # Tailwind configuration
├── clear_data.py           # Utility to reset database
├── setup.bat               # Windows setup script
├── start-backend.bat       # Windows backend starter
├── start-frontend.bat      # Windows frontend starter
└── README.md              # This file
```

---

## Usage

### Basic Analysis

1. **Enter Content**:
   - Paste text directly, or
   - Enter a URL to fetch content automatically

2. **Add Target Keyword** (optional):
   - Improves SERP and differentiation analysis

3. **Click "Analyze Content"**:
   - Wait for comprehensive analysis across all dimensions

4. **Review Results**:
   - Overall quality score
   - Individual module scores
   - Actionable recommendations

### Advanced Features

#### Batch Analysis
- Switch to **Batch Analyzer** tab
- Enter multiple URLs (one per line)
- Track progress in real-time
- Export results as CSV

#### History & Progress
- View past analyses
- Track score improvements over time
- Filter by keyword or URL
- Analyze trends with interactive charts

#### AI-Powered Improvements
- Click **Get AI Suggestions** after analysis
- Review priority actions
- Use **Rewrite Tool** to improve specific sections
- Copy improved content with one click

#### Content Comparison
- Compare your content with #1 ranking competitor
- Identify missing topics and elements
- Get structured gap analysis
- Follow step-by-step action plan

#### Export & Share
- **PDF Export**: Download professional audit report
- **Share Link**: Create public link with 30-day expiration

---

## API Documentation

### Analyze Content
```http
POST /api/analyze
Content-Type: application/json

{
  "input": "Your content text or URL",
  "target_keyword": "optional keyword"
}
```

**Response**: Comprehensive analysis with scores and recommendations

### Batch Analysis
```http
POST /api/batch/create
Content-Type: application/json

{
  "name": "Batch Name",
  "urls": ["url1", "url2", "url3"]
}
```

### Get History
```http
GET /api/history?limit=10&keyword=seo
```

### Export PDF
```http
POST /api/export-pdf
Content-Type: application/json

{
  // Analysis results object
}
```

### AI Suggestions
```http
POST /api/ai/suggestions
Content-Type: application/json

{
  "content": "Your content",
  "analysis_results": { /* analysis object */ }
}
```

### Clear Data
```http
POST /api/clear-data
```

---

## Windows Quick Setup

For Windows users, use the provided batch files:

```bash
# Initial setup
setup.bat

# Start backend
start-backend.bat

# Start frontend (in new terminal)
start-frontend.bat
```

---

## Maintenance

### Clear All Data
```bash
# Using Python script
python clear_data.py

# Or via Admin panel
# Navigate to Admin tab → Click "Clear All Data"
```

### Update Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **NLTK** - Natural Language Processing
- **TextBlob** - Sentiment Analysis
- **spaCy** - Entity Recognition
- **Groq** - Fast AI Inference
- **Google Gemini** - Advanced AI Models
- **Recharts** - Data Visualization
- **Tailwind CSS** - Modern UI Design

---

## Support

For issues, questions, or contributions:

- **GitHub Issues**: [Report a bug](https://github.com/your-username/Content_Audit_Tool/issues)
- **Discussions**: [Join the community](https://github.com/your-username/Content_Audit_Tool/discussions)

---

## Roadmap

- [ ] Multi-language support
- [ ] Custom scoring weights
- [ ] WordPress plugin integration
- [ ] Chrome extension
- [ ] Advanced competitor tracking
- [ ] Automated content scheduling
- [ ] Team collaboration features
- [ ] API rate limiting & authentication

---

**Built for BEASTBOYZ PROJECT** | **Powered by AI Analysis**
