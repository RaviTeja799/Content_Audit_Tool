# Vercel Deployment Guide - Full Stack

## Vercel Dashboard Configuration

### Project Settings:
```
Framework Preset: Other
Root Directory: ./
Build Command: (leave empty - vercel.json handles builds)
Output Directory: (leave empty)
Install Command: (leave empty - vercel.json handles installs)
```

### Environment Variables:
Add these in Vercel Dashboard → Settings → Environment Variables:

```
SERPER_API_KEY=your_actual_serper_key
GROQ_API_KEY=your_actual_groq_key
GEMINI_API_KEY=your_actual_gemini_key
FLASK_ENV=production
FLASK_DEBUG=False
```

**IMPORTANT:** 
- Remove `EXAMPLE_NAME` if it exists
- Set `FLASK_DEBUG=False` (not `True`)
- Set `FLASK_ENV=production` (not `development`)

## How It Works

1. **Backend (API)**: Deploys as serverless function at `/api/*` routes
2. **Frontend**: Builds static React app and serves from root `/`
3. **Routing**: `vercel.json` handles all routing automatically

## Deployment Steps

### Option A: Via Vercel Dashboard (Current)
1. Set Root Directory to `./` (project root)
2. Add environment variables as shown above
3. Click "Deploy"

### Option B: Via CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Add environment variables (if not done in dashboard)
vercel env add SERPER_API_KEY
vercel env add GROQ_API_KEY
vercel env add GEMINI_API_KEY
vercel env add FLASK_ENV
vercel env add FLASK_DEBUG

# Deploy to production
vercel --prod
```

## Testing After Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Test API: `https://your-project.vercel.app/api/health`
3. Test frontend: Main page should load

## Troubleshooting

### Backend Issues:
- Check function logs in Vercel Dashboard → Deployments → Your Deployment → Function Logs
- Ensure all environment variables are set
- Check that `api/requirements.txt` has all dependencies

### Frontend Issues:
- Check build logs in Vercel Dashboard
- Ensure frontend/.env.production is properly configured
- API calls should use relative path `/api`

### Common Errors:

**"Module not found"**
- Check `api/requirements.txt` includes all dependencies
- Verify PYTHONPATH is set correctly

**"404 on API calls"**
- Ensure routes in `vercel.json` are correct
- Check API calls use `/api` prefix

**"Function timeout"**
- NLTK downloads may cause cold starts
- Consider pre-downloading data in build

## File Structure (Production)

```
/api/*              → Backend Flask API (serverless)
/static/*           → Frontend static assets
/*.{js,css,etc}     → Frontend files
/*                  → Frontend index.html (catch-all)
```

## Important Notes

1. **SQLite Database**: Will be ephemeral (resets between deployments)
   - Consider using external database for production
   - Or accept that history resets on each deploy

2. **NLTK Data**: Downloads on first request
   - May cause slow first response
   - Consider pre-downloading in build step

3. **File Uploads**: Temporary storage only
   - Files don't persist between function invocations

4. **API Keys**: Never commit to Git
   - Always use Vercel environment variables
   - Verify `.env` is in `.gitignore`

## Local Development vs Production

### Local:
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`
- Separate processes

### Vercel:
- Everything: `https://your-project.vercel.app`
- Frontend serves from root
- Backend at `/api/*`
- Single unified deployment

---

**Status:** Ready for deployment ✓
