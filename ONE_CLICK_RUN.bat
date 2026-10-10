@echo off
cd /d "%~dp0"
title Smart Project Manager Assistant (SPMA)

if exist "C:\Program Files\Python311\python.exe" goto :run_server
python --version >nul 2>nul
if %errorlevel% equ 0 goto :run_server
py -3.11 --version >nul 2>nul
if %errorlevel% equ 0 goto :run_server
py -3 --version >nul 2>nul
if %errorlevel% equ 0 goto :run_server

cls
echo =======================================================================
echo   Smart Project Manager Assistant (SPMA) - Auto Setup
echo =======================================================================
echo.
echo   Configuring execution environment automatically...
echo   Please wait about 20-30 seconds (no action needed)...
echo.

if exist "%~dp0setup\python-3.11.9-amd64.exe" (
    "%~dp0setup\python-3.11.9-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
) else (
    where winget >nul 2>nul
    if %errorlevel% equ 0 (
        winget install --id Python.Python.3.11 -e --silent --accept-package-agreements --accept-source-agreements
    )
)

echo Environment ready! Starting server...
timeout /t 3 >nul 2>nul

:run_server
call START_SERVER.bat
