@echo off
cd /d "%~dp0"
title Push SPMA to GitHub (Smart-Assistant)

echo =======================================================================
echo   SPMA - Push Code to GitHub Repository
echo =======================================================================
echo.
echo Pushing clean code to GitHub...
mingit\cmd\git.exe push -u origin main --force

echo.
echo =======================================================================
echo   Done! Check your GitHub page in the browser.
echo =======================================================================
pause
