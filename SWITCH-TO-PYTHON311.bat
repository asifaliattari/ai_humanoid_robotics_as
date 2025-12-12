@echo off
echo ============================================
echo   SWITCHING TO PYTHON 3.11 (SQLAlchemy Fix)
echo ============================================
echo.

cd /d D:\hakathon\ai_humanoid_robotics_as\backend

echo [1] Checking if Python 3.11 is available...
py -3.11 --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Python 3.11 is NOT installed!
    echo.
    echo Please download and install Python 3.11 from:
    echo https://www.python.org/downloads/release/python-3119/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

py -3.11 --version
echo ✅ Python 3.11 found!
echo.

echo [2] Removing old virtual environment...
if exist ".venv" (
    rmdir /s /q .venv
    echo    Removed .venv
)
if exist "venv" (
    rmdir /s /q venv
    echo    Removed venv
)
echo ✅ Old venv removed
echo.

echo [3] Creating new virtual environment with Python 3.11...
py -3.11 -m venv .venv
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create venv
    pause
    exit /b 1
)
echo ✅ New .venv created with Python 3.11
echo.

echo [4] Activating virtual environment...
call .venv\Scripts\activate.bat
echo ✅ Activated
echo.

echo [5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✅ Pip upgraded
echo.

echo [6] Installing dependencies...
echo    This may take 1-2 minutes...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  Some packages may have failed. Trying essential packages...
    pip install fastapi uvicorn openai qdrant-client pydantic pydantic-settings python-dotenv
)
echo.
echo ✅ Dependencies installed
echo.

echo [7] Testing SQLAlchemy import...
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__} - OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ SQLAlchemy still failing
    pause
    exit /b 1
)
echo ✅ SQLAlchemy works!
echo.

echo [8] Testing main app import...
python -c "from main import app; print('Main app import - OK')"
if %ERRORLEVEL% EQU 0 (
    echo ✅ Main app works!
    echo.
    echo ============================================
    echo   SUCCESS! Backend is ready to run
    echo ============================================
    echo.
    echo To start the backend, run:
    echo   START-BACKEND-311.bat
    echo.
    echo Or manually:
    echo   cd backend
    echo   .venv\Scripts\activate
    echo   uvicorn main:app --reload --port 8000
    echo.
) else (
    echo.
    echo ⚠️  Main app has issues, but trying simple backend...
    python -c "from config import settings; print('Config OK')"
    echo.
    echo You can try running the simple backend instead:
    echo   uvicorn main-simple:app --reload --port 8000
    echo.
)

pause
