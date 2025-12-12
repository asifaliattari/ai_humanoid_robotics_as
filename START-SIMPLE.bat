@echo off
color 0B
echo.
echo ================================================
echo STARTING FRONTEND
echo ================================================
echo.

REM Check if node_modules exists
if not exist node_modules (
    echo Installing frontend packages...
    echo This takes 2-3 minutes first time...
    call npm install
)

echo.
echo Starting Docusaurus...
echo Website will open at: http://localhost:3000
echo.
echo Press Ctrl+C to stop
echo.

npm start
