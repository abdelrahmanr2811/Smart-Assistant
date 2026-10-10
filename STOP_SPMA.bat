@echo off
title Stop SPMA Background Server
echo Stopping SPMA Background Server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo [OK] SPMA Server stopped successfully.
pause
