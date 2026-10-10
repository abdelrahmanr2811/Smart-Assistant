@echo off
setlocal
chcp 65001 >nul
echo ================================================================
echo    Smart Assistant (SPMA) Service Status Check
echo ================================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { $port = 8000; $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue; if ($conn) { $pids = $conn | Select-Object -ExpandProperty OwningProcess -Unique; Write-Host '● Service State: RUNNING (ONLINE)' -ForegroundColor Green; Write-Host ('● Listening Port: 8000 (Process PID: ' + ($pids -join ', ') + ')') -ForegroundColor Green; try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/' -TimeoutSec 3; Write-Host '● API Health:    200 OK (Healthy)' -ForegroundColor Green; Write-Host '● Web URL:       http://127.0.0.1:8000/' -ForegroundColor Cyan } catch { Write-Host '● API Status:    Starting up...' -ForegroundColor Yellow } } else { Write-Host '○ Service State: STOPPED (OFFLINE)' -ForegroundColor Red; Write-Host '  To start: run start_service.bat or install_service.bat' -ForegroundColor Yellow }; Write-Host ''; Write-Host '● Windows Task Scheduler:'; $task = schtasks /Query /TN 'SmartAssistantSPMA' 2>$null; if ($task) { Write-Host '  Auto-Start on Boot: ENABLED (Task: SmartAssistantSPMA)' -ForegroundColor Green } else { Write-Host '  Auto-Start on Boot: NOT INSTALLED' -ForegroundColor Gray } }"

echo.
echo ================================================================
pause
