@echo off
echo ========================================
echo Starting Frontend Development Server...
echo ========================================
cd /d "%~dp0frontend"
call npm start
pause
