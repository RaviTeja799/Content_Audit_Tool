@echo off
echo ========================================
echo Content Quality Audit Tool - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Step 1: Setting up Python virtual environment...
cd backend
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Step 2: Installing Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip setuptools
pip install -r requirements.txt

echo.
echo Step 3: Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

echo.
echo Step 4: Installing Node.js dependencies...
cd ..\frontend
call npm install

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Run: start-backend.bat
echo   2. Run: start-frontend.bat
echo.
pause
