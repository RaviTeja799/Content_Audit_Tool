# 🔧 Troubleshooting Guide

## Current Status: ✅ WORKING!

Your application is now running successfully:
- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000 (should open automatically)

---

## Understanding the "Errors" You Saw

### 1. ✅ Markdown Linting Warnings (Cosmetic Only)
These are **NOT real errors** - just VS Code style suggestions:
- `MD022`, `MD032`, `MD040` - Formatting suggestions for README files
- **Impact**: NONE - Documentation works perfectly
- **Action**: Ignore these or disable markdown linting in VS Code

### 2. ✅ Import Resolution Warnings (VS Code Issue)
```
Import "flask_cors" could not be resolved
Import "textstat" could not be resolved
```
- **Cause**: VS Code doesn't know about your virtual environment
- **Reality**: All packages ARE installed and working
- **Action**: Configure VS Code Python interpreter or ignore

### 3. ⚠️ setuptools Warning (Fixed)
```
ModuleNotFoundError: No module named 'pkg_resources'
```
- **Cause**: Missing setuptools package
- **Solution**: Already installed with `pip install setuptools`
- **Status**: ✅ FIXED

### 4. ⚠️ Deprecation Warning (Harmless)
```
pkg_resources is deprecated as an API
```
- **Cause**: textstat library uses old API
- **Impact**: None - just a future warning
- **Action**: Ignore - will be fixed when textstat updates

---

## How to Start the Application

### Option 1: Double-Click Batch Files ✨ (Easiest)

1. **Start Backend**:
   - Double-click: `start-backend.bat`
   - Wait for "Running on http://127.0.0.1:5000"

2. **Start Frontend** (in new window):
   - Double-click: `start-frontend.bat`
   - Browser opens automatically to http://localhost:3000

### Option 2: PowerShell Commands

**Backend Terminal:**
```powershell
cd E:\BEASTBOYZ-PROJECT\backend
.\venv\Scripts\activate
python app.py
```

**Frontend Terminal (new window):**
```powershell
cd E:\BEASTBOYZ-PROJECT\frontend
npm start
```

---

## Common Issues & Solutions

### Issue: "Cannot find path 'backend\backend'"
**Cause**: Running command from wrong directory
**Solution**: Use absolute paths or the updated batch files

### Issue: "Port 5000 already in use"
**Cause**: Another Flask app is running
**Solution**: 
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or change port in backend/app.py line 79
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: "Port 3000 already in use"
**Cause**: Another React app is running
**Solution**: When prompted, press 'Y' to use a different port

### Issue: Frontend can't connect to backend
**Symptoms**: CORS errors, network errors
**Solution**: 
1. Ensure backend is running on port 5000
2. Check backend console for errors
3. Test backend: http://localhost:5000/api/health

### Issue: "npm: command not found"
**Cause**: Node.js not installed
**Solution**: 
1. Install Node.js from https://nodejs.org/
2. Restart terminal
3. Run `node --version` to verify

### Issue: "python: command not found"
**Cause**: Python not in PATH
**Solution**: 
1. Install Python from https://python.org/
2. Check "Add Python to PATH" during installation
3. Restart terminal

---

## Testing the Application

### 1. Test Backend API

Open PowerShell:
```powershell
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status":"healthy","message":"Content Audit API is running"}
```

### 2. Test Full Analysis

1. Open browser: http://localhost:3000
2. Paste sample text:
   ```
   Best Budget Laptops 2025
   
   Looking for affordable laptops? Here are the top budget options 
   that won't break the bank. We tested 15 models to find the best 
   value for students and professionals.
   ```
3. Target keyword: `best budget laptops`
4. Click "Analyze Content"
5. Wait 30-60 seconds
6. See results with 5 scores!

### 3. Test URL Analysis

1. Enter URL: `https://example.com` (or any public article)
2. Target keyword: relevant keyword
3. Analyze

---

## VS Code Configuration (Optional)

To fix import warnings in VS Code:

1. **Press**: `Ctrl + Shift + P`
2. **Type**: "Python: Select Interpreter"
3. **Choose**: `.\venv\Scripts\python.exe`

This tells VS Code about your virtual environment.

---

## Performance Notes

### First Analysis
- Takes 30-60 seconds
- Downloads NLTK data
- Scrapes SERP results

### Subsequent Analyses
- Faster (15-30 seconds)
- NLTK data cached
- Only SERP scraping takes time

### SERP Scraping
If Google blocks requests:
- Tool uses fallback mock data
- Other analyses still work
- Results are still useful

---

## Verification Checklist

Run these to verify everything works:

```powershell
# 1. Check Python packages
cd E:\BEASTBOYZ-PROJECT\backend
.\venv\Scripts\activate
pip list | findstr "flask textstat nltk"

# 2. Check Node packages
cd E:\BEASTBOYZ-PROJECT\frontend
npm list react axios

# 3. Test backend
cd E:\BEASTBOYZ-PROJECT\backend
.\venv\Scripts\activate
python app.py
# Open http://localhost:5000/api/health

# 4. Test frontend
cd E:\BEASTBOYZ-PROJECT\frontend
npm start
# Opens http://localhost:3000
```

---

## Cleaning Up

### Stop Servers
- **Backend**: Press `Ctrl + C` in backend terminal
- **Frontend**: Press `Ctrl + C` in frontend terminal

### Full Restart
```powershell
# Stop all
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Start fresh
# Run start-backend.bat
# Run start-frontend.bat
```

---

## Log Files Location

### Backend Logs
- Console output in PowerShell terminal
- Flask debug logs shown in real-time

### Frontend Logs
- Browser console (F12 → Console tab)
- Network tab shows API calls

---

## Getting Help

### Check Backend Status
```powershell
curl http://localhost:5000/api/health
```

### Check Frontend Status
Open browser to: http://localhost:3000

### View API Errors
Look at backend PowerShell terminal

### View Frontend Errors
Press F12 in browser → Console tab

---

## Summary of Fixes Applied

✅ **Installed setuptools** - Fixed pkg_resources error
✅ **Updated batch files** - Fixed path issues
✅ **Verified all packages** - Everything installed correctly
✅ **Both servers running** - Backend + Frontend working

---

## Current Status

```
✅ Backend: Running on http://localhost:5000
✅ Frontend: Running on http://localhost:3000
✅ All dependencies installed
✅ Ready to analyze content!
```

---

## Next Steps

1. Keep both terminals open
2. Open http://localhost:3000 in browser
3. Enter content or URL
4. Add target keyword (optional)
5. Click "Analyze Content"
6. Review your comprehensive audit!

---

**🎉 Your Content Quality Audit Tool is fully operational!**
