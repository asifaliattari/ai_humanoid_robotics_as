@echo off
echo ========================================
echo Starting Frontend Server
echo ========================================
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo [ERROR] node_modules not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)

echo Starting Docusaurus development server...
echo Website will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

npm start
