@echo off
echo ========================================
echo Backend Debug - Check Setup
echo ========================================
echo.

cd backend

echo [1] Checking virtual environment...
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup-windows.bat first
    pause
    exit /b 1
)
echo [OK] Virtual environment exists
echo.

echo [2] Checking .env file...
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env
    pause
    exit /b 1
)
echo [OK] .env file exists
echo.

echo [3] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

echo [4] Checking Python packages...
python -c "import fastapi; print('[OK] FastAPI installed')" 2>nul || echo [ERROR] FastAPI not installed
python -c "import sqlalchemy; print('[OK] SQLAlchemy installed')" 2>nul || echo [ERROR] SQLAlchemy not installed
python -c "import qdrant_client; print('[OK] Qdrant client installed')" 2>nul || echo [ERROR] Qdrant client not installed
python -c "import openai; print('[OK] OpenAI installed')" 2>nul || echo [ERROR] OpenAI not installed
echo.

echo [5] Checking configuration...
python -c "from config import settings; print('[OK] Config loaded successfully'); print('App:', settings.app_name)" 2>nul
if errorlevel 1 (
    echo [ERROR] Config failed to load!
    echo Check your .env file for errors
    echo.
    python -c "from config import settings"
    pause
    exit /b 1
)
echo.

echo [6] Testing API imports...
python -c "from api.rag import book_qa_router, selection_qa_router; print('[OK] RAG API imports work')" 2>nul
if errorlevel 1 (
    echo [ERROR] API import failed!
    echo.
    python -c "from api.rag import book_qa_router"
    pause
    exit /b 1
)
echo.

echo [7] Testing database connection...
python -c "from models import engine; print('[OK] Database engine created')" 2>nul
if errorlevel 1 (
    echo [ERROR] Database connection failed!
    echo Check your DATABASE_URL in .env
    pause
    exit /b 1
)
echo.

echo ========================================
echo All checks passed!
echo ========================================
echo.
echo Starting backend with detailed logging...
echo Press Ctrl+C to stop
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
