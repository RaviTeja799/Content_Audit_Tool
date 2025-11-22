# Vercel Deployment Configuration

## Environment Variables

Add these environment variables in your Vercel project settings:

### Required API Keys
```
SERPER_API_KEY=your_serper_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional Configuration
```
FLASK_ENV=production
FLASK_DEBUG=False
```

## Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Add Environment Variables**:
   - Go to your Vercel project dashboard
   - Navigate to Settings > Environment Variables
   - Add all required API keys

5. **Redeploy** (if needed):
   ```bash
   vercel --prod
   ```

## Important Notes

- The backend runs as a serverless function on Vercel
- Database files (SQLite) will be ephemeral - consider using a managed database for production
- File uploads and PDF generation work with temporary storage
- NLTK data is downloaded on first request (may cause cold start delays)

## Alternative: Separate Deployments

For better performance, consider:
- **Frontend**: Deploy on Vercel
- **Backend**: Deploy on Railway, Render, or DigitalOcean
- Update `REACT_APP_API_URL` in frontend to point to backend URL
