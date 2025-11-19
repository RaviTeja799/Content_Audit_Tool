# Content Quality Audit Tool - Setup Guide

## Quick Start

### 1. Install Backend Dependencies

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download NLTK Data

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

### 3. Start Backend Server

```powershell
python app.py
```

The backend will run on `http://localhost:5000`

### 4. Install Frontend Dependencies

Open a new terminal:

```powershell
cd frontend
npm install
```

### 5. Start Frontend

```powershell
npm start
```

The frontend will open automatically at `http://localhost:3000`

## Features Overview

### 1. SEO Score (0-100)
- Keyword density analysis
- Readability metrics (Flesch-Kincaid)
- Header structure validation
- Meta description check
- Content length assessment

### 2. SERP Performance Score (0-100)
- Compares against top 10 SERP results
- Word count comparison
- Topic coverage analysis
- Content element detection (comparisons, data, lists)
- Predicts ranking position

### 3. AEO Score (0-100)
- Citation quality check
- Structured formatting (FAQ, lists, tables)
- Answer-style content patterns
- Question coverage
- AI-friendly patterns

### 4. Humanization Score (0-100)
- Sentence variety analysis
- AI pattern detection
- Natural flow assessment
- Vocabulary diversity
- Conversational elements

### 5. Differentiation Score (0-100)
- Content overlap vs competitors
- Unique element detection
- Structural differentiation
- Value proposition analysis

## Usage

1. **Enter Content**: Paste text or enter a URL
2. **Add Target Keyword** (optional but recommended)
3. **Click "Analyze Content"**
4. **Wait 30-60 seconds** for complete analysis
5. **Review Results**: See scores, issues, and recommendations

## Example Input

### Text Input:
```
# Best Budget Laptops 2025

Looking for affordable computing? Here are the top budget laptops...
```

### URL Input:
```
https://example.com/blog/best-budget-laptops-2025
```

### Target Keyword:
```
best budget laptops 2025
```

## Troubleshooting

### Backend Issues

**Error: Module not found**
```powershell
pip install -r requirements.txt
```

**Error: NLTK data not found**
```powershell
python -c "import nltk; nltk.download('all')"
```

**Port 5000 already in use**
Edit `backend/app.py` line 79:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Frontend Issues

**Error: npm command not found**
Install Node.js from https://nodejs.org/

**Port 3000 already in use**
The app will prompt to use a different port automatically.

**CORS errors**
Make sure backend is running on port 5000.

## API Endpoints

### Health Check
```
GET http://localhost:5000/api/health
```

### Analyze Content
```
POST http://localhost:5000/api/analyze
Content-Type: application/json

{
  "input": "Your content or URL",
  "target_keyword": "optional keyword"
}
```

## Architecture

```
BEASTBOYZ-PROJECT/
├── backend/
│   ├── app.py                      # Flask API server
│   ├── analyzers/
│   │   ├── seo_analyzer.py         # SEO metrics
│   │   ├── serp_analyzer.py        # SERP comparison
│   │   ├── aeo_analyzer.py         # AEO metrics
│   │   ├── humanization_analyzer.py # Human writing patterns
│   │   └── differentiation_analyzer.py # Uniqueness
│   └── utils/
│       ├── text_extractor.py       # Extract from URL/text
│       └── serp_scraper.py         # Google SERP scraping
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── InputForm.js        # Content input
│       │   ├── ResultsDashboard.js # Results display
│       │   ├── ScoreCard.js        # Individual score cards
│       │   └── LoadingSpinner.js   # Loading state
│       └── App.js                  # Main component
└── README.md
```

## Performance Notes

- SERP analysis may take 30-60 seconds (fetching competitor data)
- First analysis downloads NLTK data automatically
- Recommended: Use target keyword for best results
- URLs must be publicly accessible

## Future Enhancements

- [ ] Export results as PDF
- [ ] Historical tracking
- [ ] Bulk URL analysis
- [ ] More detailed competitor comparison
- [ ] Schema markup detection
- [ ] Mobile readability scoring
- [ ] Internal linking analysis

## Support

For issues or questions, check the console output in both terminals for detailed error messages.
