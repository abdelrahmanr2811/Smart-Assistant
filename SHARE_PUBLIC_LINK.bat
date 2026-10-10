@echo off
cd /d "%~dp0"
title SPMA - Online Public Link Generator

python publish_link.py
if errorlevel 1 (
    echo.
    echo Trying fallback SSH tunnel...
    where ssh >nul 2>nul
    if %errorlevel% equ 0 (
        ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 serveo.net
    ) else (
        "%SystemRoot%\System32\OpenSSH\ssh.exe" -o StrictHostKeyChecking=no -R 80:localhost:8000 serveo.net
    )
)
pause
