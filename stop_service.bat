@echo off
setlocal
chcp 65001 >nul

echo ================================================================
echo    Stopping Smart Assistant (SPMA) Windows Service...
echo ================================================================

schtasks /End /TN "SmartAssistantSPMA" >nul 2>&1

powershell -NoProfile -ExecutionPolicy Bypass -Command "& { $port = 8000; $pids = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if ($pids) { foreach ($p in $pids) { Write-Host ('[*] Stopping process on port 8000 (PID: ' + $p + ')...'); Stop-Process -Id $p -Force -ErrorAction SilentlyContinue }; Write-Host '[OK] Service stopped successfully.' -ForegroundColor Green } else { Write-Host '[INFO] No running service found on port 8000.' -ForegroundColor Yellow } }"

echo.
timeout /t 2 >nul
