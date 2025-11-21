# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- Python 3.11+ installed ([Download](https://www.python.org/downloads/))
- Node.js 16+ and npm ([Download](https://nodejs.org/))
- Git installed ([Download](https://git-scm.com/downloads))

## Installation

### Windows Users (Easiest Method)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Content_Audit_Tool.git
cd Content_Audit_Tool

# 2. Run automated setup
setup.bat

# 3. Configure API keys
cd backend
notepad .env
# Add your API keys and save

# 4. Start the application
cd ..
start-backend.bat    # Terminal 1
start-frontend.bat   # Terminal 2
```

### Manual Setup (All Platforms)

#### Backend Setup
```bash
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

# Install TextBlob data
python -m textblob.download_corpora

# Configure environment
cp .env.example .env
nano .env  # or use your preferred editor

# Start backend
python app.py
```

Backend runs at: `http://localhost:5000`

#### Frontend Setup
```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: `http://localhost:3000`

## Getting API Keys (5 minutes)

### 1. Serper.dev (Required for SERP analysis)
1. Go to [serper.dev](https://serper.dev/)
2. Sign up (Google OAuth)
3. Get 2,500 free searches
4. Copy API key to `.env` as `SERPER_API_KEY`

### 2. Groq (Required for AI suggestions)
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up/Login
3. Navigate to API Keys
4. Create new key
5. Copy to `.env` as `GROQ_API_KEY`

### 3. Google Gemini (Optional - AI improvements)
1. Go to [ai.google.dev](https://ai.google.dev/)
2. Click "Get API Key"
3. Create key in Google AI Studio
4. Copy to `.env` as `GEMINI_API_KEY`

## Verify Installation

Once both servers are running:

1. Open browser to `http://localhost:3000`
2. You should see the Content Quality Audit Tool
3. Try a sample analysis:
   - Enter: "Artificial Intelligence is transforming modern technology"
   - Click "Analyze Content"
   - Wait for results

## First Analysis

### Test with URL
```
URL: https://www.example.com/your-article
Keyword: your target keyword
```

### Test with Text
```
Paste a blog post or article (500+ words recommended)
Add target keyword for better insights
```

## Features to Try

After your first analysis:

1. **Export PDF**: Click "Export PDF" button
2. **View History**: Switch to "History & Progress" tab
3. **Batch Analysis**: Try analyzing multiple URLs
4. **AI Suggestions**: Click "Get AI Suggestions"
5. **Content Comparison**: Compare with top competitor

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### NLTK errors
```bash
# Manually download all NLTK data
python -c "import nltk; nltk.download('all')"
```

### Port already in use
```bash
# Backend (port 5000)
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Frontend (port 3000)
# Kill process using port 3000 and restart
```

## Access from Mobile

1. Find your computer's local IP:
   ```bash
   # Windows
   ipconfig
   # Look for IPv4 Address

   # macOS/Linux
   ifconfig
   # Look for inet address
   ```

2. Update frontend to use IP:
   - Edit `frontend/src/App.js`
   - Change `http://localhost:5000` to `http://YOUR_IP:5000`

3. Access from mobile: `http://YOUR_IP:3000`

## Next Steps

1. **Read the [README.md](README.md)** for detailed documentation
2. **Check [CONTRIBUTING.md](CONTRIBUTING.md)** if you want to contribute
3. **Review [API Documentation](#)** for integration
4. **Join discussions** for support and feature requests

## Pro Tips

- **Save time**: Use batch analysis for multiple URLs
- **Track progress**: Regular analysis shows improvement trends
- **AI assistance**: Use AI suggestions for quick wins
- **Export reports**: PDF exports are great for client presentations
- **Bookmark**: Add to favorites for quick access

## Need Help?

- [Full Documentation](README.md)
- [Report Issues](https://github.com/your-username/Content_Audit_Tool/issues)
- [Community Discussions](https://github.com/your-username/Content_Audit_Tool/discussions)

---

**Total Setup Time**: ~5 minutes  
**First Analysis**: ~30 seconds  
**Master All Features**: ~10 minutes

Happy Analyzing!
