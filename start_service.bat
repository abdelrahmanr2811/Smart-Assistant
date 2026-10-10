@echo off
setlocal
chcp 65001 >nul

echo Starting Smart Assistant Background Service...
wscript.exe "%~dp0start_service_hidden.vbs"

echo Waiting for service to initialize...
timeout /t 3 /nobreak >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/' -TimeoutSec 3; Write-Host '[OK] Service is ONLINE at http://127.0.0.1:8000/' -ForegroundColor Green } catch { Write-Host '[!] Service is starting in background...' -ForegroundColor Yellow } }"

echo.
echo Service running in background.
timeout /t 2 >nul
