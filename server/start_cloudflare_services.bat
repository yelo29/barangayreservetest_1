@echo off
echo ========================================
echo   BARANGAY RESERVE - CLOUDFLARE TUNNEL
echo ========================================
echo.

echo Configuration Status:
echo    Android App: https://barangay-reserve.trycloudflare.com
echo    Server: Python on port 8000
echo    Tunnel: Cloudflare (free, no limits)
echo.

echo Starting Services...
echo.

REM Start Python Server
echo Starting Python server on port 8000...
cd /d "%~dp0"
start "Python Server" cmd /k python server.py

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Start Cloudflare Tunnel
echo Starting Cloudflare tunnel...
cd /d "C:\tools\cloudflare"
start "Cloudflare Tunnel" cmd /k .\cloudflared.exe tunnel --url http://localhost:8000

echo.
echo Both services started!
echo Android app ready: https://barangay-reserve.trycloudflare.com
echo Tunnel URL will be shown in Cloudflare window
echo.
pause