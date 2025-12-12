@echo off
echo ========================================
echo Physical AI Book - Start All Servers
echo ========================================
echo.

REM Check if setup was run
if not exist "backend\venv" (
    echo [ERROR] Backend not set up!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo [ERROR] Frontend not set up!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

if not exist "backend\.env" (
    echo [ERROR] Configuration missing!
    echo Please edit backend\.env with your API keys
    pause
    exit /b 1
)

echo Starting both servers...
echo.
echo Backend will run at: http://localhost:8000
echo Frontend will run at: http://localhost:3000
echo.
echo Press Ctrl+C in this window to stop ALL servers
echo.

REM Start backend in a new window
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait 3 seconds for backend to start
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
start "Frontend Server" cmd /k "npm start"

echo.
echo ========================================
echo Servers started!
echo ========================================
echo.
echo Two new windows opened:
echo  1. Backend Server (port 8000)
echo  2. Frontend Server (port 3000)
echo.
echo Your website will open automatically in a few seconds...
echo.
echo To stop servers: Close the terminal windows or press Ctrl+C
echo.
pause
