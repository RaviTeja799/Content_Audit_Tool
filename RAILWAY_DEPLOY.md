# Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Click "Login" and sign in with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose: `RaviTeja799/Content_Audit_Tool`
4. Railway will automatically detect the Dockerfile

### Step 3: Add Environment Variables
Click on your service → Variables tab → Add these:

```
SERPER_API_KEY=your_serper_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
```

**Get your API keys from:**
- SERPER_API_KEY: https://serper.dev/
- GROQ_API_KEY: https://console.groq.com/
- GEMINI_API_KEY: https://ai.google.dev/

### Step 4: Deploy
- Click "Deploy"
- Wait 3-5 minutes for first build
- Railway will provide a URL like: `https://content-audit-tool.railway.app`

### Step 5: Test Your Deployment
- Visit: `https://your-app.railway.app/api/health`
- Should return: `{"status": "healthy"}`

## Files Created for Railway

✅ **Dockerfile** - Containerizes the Flask backend
✅ **railway.json** - Railway configuration
✅ **.dockerignore** - Excludes unnecessary files from build

## What Gets Deployed

- ✅ Backend Flask API (all routes work)
- ✅ All 9 analysis modules
- ✅ AI integrations (Groq, Gemini)
- ✅ SQLite database (persistent storage)
- ✅ PDF generation
- ✅ History tracking

## For Frontend

### Option 1: Run Locally (Easiest for Demo)
```bash
cd frontend
npm start
```
Update `frontend/src/App.js`:
```javascript
const API_URL = 'https://your-app.railway.app';
```

### Option 2: Deploy Frontend on Netlify
1. Build frontend: `cd frontend && npm run build`
2. Go to [netlify.com](https://netlify.com)
3. Drag & drop the `frontend/build` folder
4. Done!

## Cost
- **Railway Free Tier**: $5 credit/month
- **Enough for**: Hackathon demo + 2-3 weeks of testing
- **After free tier**: ~$5/month

## Troubleshooting

### Build Failed
- Check Railway logs in dashboard
- Ensure all files are committed to GitHub
- Verify Dockerfile syntax

### API Not Working
- Check environment variables are set
- View logs in Railway dashboard
- Test health endpoint first

### Database Issues
- Railway provides persistent storage
- SQLite files persist between deployments
- Clear data using `/api/clear-data` endpoint if needed

---

**Ready to deploy!** Just follow the steps above.
