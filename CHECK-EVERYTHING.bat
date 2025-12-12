@echo off
echo ========================================
echo CHECKING EVERYTHING
echo ========================================
echo.

cd backend

echo [1] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [2] Checking Python version...
python --version
echo.

echo [3] Testing OpenAI connection...
python -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('[OK] OpenAI connected')"
if errorlevel 1 (
    echo [ERROR] OpenAI connection failed!
    echo.
    pause
)
echo.

echo [4] Testing Qdrant connection...
python -c "from qdrant_client import QdrantClient; import os; from dotenv import load_dotenv; load_dotenv(); client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print('[OK] Qdrant connected'); print('Collections:', client.get_collections())"
if errorlevel 1 (
    echo [ERROR] Qdrant connection failed!
    echo.
    pause
)
echo.

echo [5] Testing config loading...
python -c "from config import settings; print('[OK] Config loaded'); print('App:', settings.app_name); print('Qdrant:', settings.qdrant_url[:50]); print('Database:', settings.database_url)"
if errorlevel 1 (
    echo [ERROR] Config loading failed!
    echo.
    pause
)
echo.

echo [6] Testing main app import...
python -c "from main import app; print('[OK] Main app imported')"
if errorlevel 1 (
    echo [ERROR] Main app import failed!
    echo The error above shows what's wrong
    echo.
    pause
)
echo.

echo ========================================
echo All checks passed!
echo ========================================
echo.
echo Now try: DO-EVERYTHING.bat
pause
