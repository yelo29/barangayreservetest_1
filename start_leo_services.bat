@echo off
echo ========================================
echo   BARANGAY RESERVE - LEO'S SETUP
echo ========================================
echo.

echo ✅ Configuration Status:
echo    Android App: https://unstanding-unmenaced-pete.ngrok-free.dev
echo    Server: Python on port 8000
echo    Ngrok: Leo's account configured
echo.

echo 🚀 Starting Services...
echo.

REM Start Python Server
echo Starting Python server on port 8000...
cd /d "%~dp0server"
start "Python Server" cmd /k python server.py

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Start Ngrok
echo Starting ngrok tunnel for Leo's account...
cd /d "C:\tools\ngrok"
start "Ngrok Tunnel" cmd /k ngrok http 8000

echo.
echo ✅ Both services started!
echo 📱 Android app ready: https://unstanding-unmenaced-pete.ngrok-free.dev
echo.
pause
