@echo off
cd /d "%~dp0"
title Smart Project Manager Assistant (SPMA)

if exist "C:\Program Files\Python311\python.exe" (
    "C:\Program Files\Python311\python.exe" launcher.py
    if not errorlevel 1 goto :end
)

python launcher.py
if not errorlevel 1 goto :end

py -3.11 launcher.py
if not errorlevel 1 goto :end

py -3 launcher.py
if not errorlevel 1 goto :end

:end
pause
