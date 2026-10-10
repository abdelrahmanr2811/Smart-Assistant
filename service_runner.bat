@echo off
setlocal enabledelayedexpansion

:: Change to backend directory
cd /d "%~dp0backend"

:: Ensure logs directory exists
if not exist "logs" mkdir logs

:: Start Uvicorn in production server mode
echo [%date% %time%] Starting Smart Assistant Windows Service... >> logs\service.log
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 >> logs\service.log 2>&1
