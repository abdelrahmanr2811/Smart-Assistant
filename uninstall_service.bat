@echo off
title Uninstall Smart Assistant Windows Service
chcp 65001 >nul

echo ================================================================
echo    Uninstalling Smart Assistant (SPMA) Windows Service...
echo ================================================================

call "%~dp0stop_service.bat"

echo [*] Removing Scheduled Service Task...
schtasks /Delete /TN "SmartAssistantSPMA" /F >nul 2>&1

if %errorLevel% equ 0 (
    echo [OK] Windows Service Task removed successfully.
) else (
    echo [INFO] Service task was not found or already removed.
)

echo.
echo [DONE] Service uninstalled.
pause
