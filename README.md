# Content Quality Audit Tool

A comprehensive content analysis tool that scores text across 5 dimensions: SEO, SERP Performance, AEO, Humanization, and Differentiation.

## Features

- ✅ Analyze text or URL inputs
- ✅ SEO Score (keyword density, readability, headers, meta)
- ✅ SERP Performance Score (compare against top 10 rankings)
- ✅ AEO Score (citations, structured data, AI-friendly patterns)
- ✅ Humanization Score (natural flow, sentence variety)
- ✅ Differentiation Score (uniqueness vs competitors)
- ✅ Actionable recommendations for each metric
- ✅ Clean dashboard UI

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: React + Tailwind CSS
- **Analysis Libraries**: 
  - BeautifulSoup4 (web scraping)
  - NLTK (text analysis)
  - TextStat (readability metrics)
  - scikit-learn (text comparison)

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Usage

1. Start the backend server (runs on `http://localhost:5000`)
2. Start the frontend (runs on `http://localhost:3000`)
3. Enter text or paste a URL
4. Click "Analyze Content"
5. View your comprehensive audit report

## Project Structure

```
BEASTBOYZ-PROJECT/
├── backend/
│   ├── app.py                 # Flask API
│   ├── analyzers/
│   │   ├── seo_analyzer.py
│   │   ├── serp_analyzer.py
│   │   ├── aeo_analyzer.py
│   │   ├── humanization_analyzer.py
│   │   └── differentiation_analyzer.py
│   ├── utils/
│   │   ├── text_extractor.py
│   │   └── serp_scraper.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## API Endpoints

- `POST /api/analyze` - Analyze content (text or URL)
  - Body: `{ "input": "text or URL", "target_keyword": "optional keyword" }`
  - Response: JSON with all 5 scores and recommendations

## License

MIT
