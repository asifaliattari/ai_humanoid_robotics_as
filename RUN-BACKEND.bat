@echo off
title Backend Server
cd /d D:\hakathon\ai_humanoid_robotics_as\backend
echo Starting Backend Server...
echo.
echo API will be available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
.venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
