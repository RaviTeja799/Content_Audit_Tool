# Frontend Deployment to Vercel

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- Vercel CLI installed: `npm install -g vercel`

## Deployment Steps

### 1. Install Vercel CLI (if not installed)
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy from Frontend Directory
```bash
cd frontend
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- Project name? `content-audit-tool-frontend` (or your choice)
- In which directory is your code located? `./`
- Want to override settings? **N**

### 4. Set Environment Variable
After deployment, set the API URL:

```bash
vercel env add REACT_APP_API_URL production
```

When prompted, enter: `https://contentaudittool-production.up.railway.app`

Or via Vercel Dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add variable:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://contentaudittool-production.up.railway.app`
   - **Environment**: Production

### 5. Redeploy with Environment Variable
```bash
vercel --prod
```

## Alternative: Deploy via Vercel Dashboard

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select the `frontend` folder as root directory
4. Add environment variable:
   - **REACT_APP_API_URL** = `https://contentaudittool-production.up.railway.app`
5. Click "Deploy"

## Configuration Files

- **vercel.json**: Vercel deployment configuration
- **.env.example**: Example environment variables (copy to `.env` for local development)
- **src/config/api.js**: Centralized API URL configuration

## Local Development

1. Create `.env` file in frontend directory:
```bash
echo "REACT_APP_API_URL=https://contentaudittool-production.up.railway.app" > .env
```

2. Start development server:
```bash
npm start
```

## Notes

- The frontend is configured to use `REACT_APP_API_URL` environment variable
- Fallback URL is the Railway backend: `https://contentaudittool-production.up.railway.app`
- All API calls are now centralized through `src/config/api.js`
