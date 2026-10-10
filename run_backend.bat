@echo off
chcp 65001 >nul
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
set "PYTHONPATH=%~dp0backend;%PYTHONPATH%"
title Smart Assistant - Construction PM Backend
echo ========================================================
echo   Starting Smart Assistant AI Server (FastAPI + ChromaDB)
echo   Web Client URL: http://127.0.0.1:8000
echo   API Docs URL:   http://127.0.0.1:8000/docs
echo ========================================================
cd /d "%~dp0backend"

set "PYTHON_EXE="

if exist "C:\Program Files\Python311\python.exe" (
    set "PYTHON_EXE=C:\Program Files\Python311\python.exe"
    goto :found_python
)
if exist "C:\Program Files\Python312\python.exe" (
    set "PYTHON_EXE=C:\Program Files\Python312\python.exe"
    goto :found_python
)
if exist "C:\Program Files\Python310\python.exe" (
    set "PYTHON_EXE=C:\Program Files\Python310\python.exe"
    goto :found_python
)
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    echo "%%i" | findstr /i "WindowsApps" >nul
    if errorlevel 1 (
        set "PYTHON_EXE=%%i"
        goto :found_python
    )
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :found_python
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :found_python
)
if exist "C:\Windows\py.exe" (
    set "PYTHON_EXE=C:\Windows\py.exe"
    goto :found_python
)

:found_python
if not defined PYTHON_EXE (
    echo [ERROR] Python not found. Please install Python 3.11+.
    pause
    exit /b 1
)

"%PYTHON_EXE%" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
