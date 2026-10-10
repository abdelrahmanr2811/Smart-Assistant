@echo off
cd /d "%~dp0"
title SPMA - 1-Click Online Publisher

echo =======================================================================
echo   Smart Project Manager Assistant (SPMA) - 1-Click Online Launcher
echo =======================================================================
echo.
echo [1/2] Starting SPMA Local Server in background...
start "" wscript RUN_BACKGROUND.vbs
timeout /t 3 >nul

echo [2/2] Generating Free Online Public Link...
python publish_link.py
if errorlevel 1 (
    "%SystemRoot%\System32\OpenSSH\ssh.exe" -o StrictHostKeyChecking=no -R 80:localhost:8000 serveo.net
)
pause
