@echo off
title Smart Assistant (SPMA) - Windows Service Installer
chcp 65001 >nul
color 0B

echo ================================================================
echo    Smart Project Manager Assistant (SPMA) - Service Installer
echo    جامعة النيل الأزرق - تثبيت الخدمة الخلفية لنظام ويندوز
echo ================================================================
echo.

:: Check for Administrator Privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Requesting Administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

set "TASK_NAME=SmartAssistantSPMA"
set "RUNNER_VBS=%~dp0start_service_hidden.vbs"

echo [*] Removing any existing service task...
schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1

echo [*] Registering Windows Service Task (%TASK_NAME%)...
schtasks /Create /TN "%TASK_NAME%" /TR "wscript.exe \"%RUNNER_VBS%\"" /SC ONLOGON /RL HIGHEST /F

if %errorLevel% equ 0 (
    echo.
    echo [OK] Windows Service installed successfully!
    echo [*] Starting service now in background...
    schtasks /Run /TN "%TASK_NAME%"
    wscript.exe "%RUNNER_VBS%"
    echo.
    echo ================================================================
    echo  [SUCCESS] Service is now running in the background!
    echo  Web URL:      http://127.0.0.1:8000/
    echo  API Docs URL: http://127.0.0.1:8000/docs
    echo ================================================================
) else (
    echo.
    echo [ERROR] Failed to install Windows Service.
)

echo.
pause
