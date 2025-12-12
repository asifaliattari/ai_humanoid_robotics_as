@echo off
echo ============================================
echo   Starting Backend (Python 3.11)
echo ============================================
echo.

cd /d D:\hakathon\ai_humanoid_robotics_as\backend

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

uvicorn main:app --reload --port 8000
