@echo off
title Smart Assistant - Flutter Cross-Platform Client
echo ========================================================
echo   Running Flutter Smart Assistant App
echo   Options:
echo   1. Run on Windows Desktop: flutter run -d windows
echo   2. Run on Web Browser:     flutter run -d chrome
echo   3. Run on Android:         flutter run -d android
echo ========================================================
cd /d "%~dp0frontend"
flutter run
pause
