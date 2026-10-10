@echo off
title Restart Smart Assistant Service
chcp 65001 >nul

echo Restarting Smart Assistant Service...
call "%~dp0stop_service.bat"
timeout /t 2 /nobreak >nul
call "%~dp0start_service.bat"
