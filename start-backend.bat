@echo off
echo ========================================
echo Starting Backend Server...
echo ========================================
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
python app.py
pause
