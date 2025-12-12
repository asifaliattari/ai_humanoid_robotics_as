@echo off
echo ========================================
echo Fresh Installation - Clean Start
echo ========================================
echo.

echo [1] Checking Python version...
python --version
echo.
echo If this says Python 3.13, please install Python 3.12
echo Download from: https://www.python.org/downloads/
echo.
pause

echo [2] Removing old virtual environment...
cd backend
if exist venv (
    rmdir /s /q venv
    echo Old venv deleted
) else (
    echo No old venv found
)
echo.

echo [3] Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create venv
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

echo [4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [5] Checking Python version in venv...
python --version
echo.

echo [6] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [7] Installing packages ONE BY ONE...
echo This will show exactly which package fails
echo.

echo Installing FastAPI...
pip install fastapi==0.109.0
if errorlevel 1 (echo [FAILED] FastAPI) else (echo [OK] FastAPI)
echo.

echo Installing Uvicorn...
pip install "uvicorn[standard]==0.27.0"
if errorlevel 1 (echo [FAILED] Uvicorn) else (echo [OK] Uvicorn)
echo.

echo Installing SQLAlchemy...
pip install sqlalchemy==2.0.25
if errorlevel 1 (
    echo [FAILED] SQLAlchemy
    echo Trying without version pin...
    pip install sqlalchemy
)
if errorlevel 1 (echo [FAILED] SQLAlchemy completely) else (echo [OK] SQLAlchemy)
echo.

echo Installing Alembic...
pip install alembic==1.13.1
if errorlevel 1 (echo [FAILED] Alembic) else (echo [OK] Alembic)
echo.

echo Installing Qdrant...
pip install qdrant-client==1.7.3
if errorlevel 1 (echo [FAILED] Qdrant) else (echo [OK] Qdrant)
echo.

echo Installing AsyncPG...
pip install asyncpg==0.29.0
if errorlevel 1 (echo [FAILED] AsyncPG) else (echo [OK] AsyncPG)
echo.

echo Installing OpenAI...
pip install openai==1.10.0
if errorlevel 1 (echo [FAILED] OpenAI) else (echo [OK] OpenAI)
echo.

echo Installing Tiktoken...
pip install tiktoken==0.5.2
if errorlevel 1 (echo [FAILED] Tiktoken) else (echo [OK] Tiktoken)
echo.

echo Installing Pydantic...
pip install pydantic==2.5.3
if errorlevel 1 (echo [FAILED] Pydantic) else (echo [OK] Pydantic)
echo.

echo Installing Pydantic Settings...
pip install pydantic-settings==2.1.0
if errorlevel 1 (echo [FAILED] Pydantic Settings) else (echo [OK] Pydantic Settings)
echo.

echo Installing Python Dotenv...
pip install python-dotenv==1.0.0
if errorlevel 1 (echo [FAILED] Python Dotenv) else (echo [OK] Python Dotenv)
echo.

echo Installing HTTPx...
pip install httpx==0.26.0
if errorlevel 1 (echo [FAILED] HTTPx) else (echo [OK] HTTPx)
echo.

echo Installing Python Multipart...
pip install python-multipart==0.0.6
if errorlevel 1 (echo [FAILED] Python Multipart) else (echo [OK] Python Multipart)
echo.

echo Installing Python Jose...
pip install "python-jose[cryptography]==3.3.0"
if errorlevel 1 (echo [FAILED] Python Jose) else (echo [OK] Python Jose)
echo.

echo Installing Passlib...
pip install "passlib[bcrypt]==1.7.4"
if errorlevel 1 (echo [FAILED] Passlib) else (echo [OK] Passlib)
echo.

echo Installing Python JSON Logger...
pip install python-json-logger==2.0.7
if errorlevel 1 (echo [FAILED] Python JSON Logger) else (echo [OK] Python JSON Logger)
echo.

echo.
echo ========================================
echo Installation Summary
echo ========================================
echo.

echo Verifying critical packages...
python -c "import fastapi; print('[OK] FastAPI imported')"
python -c "import sqlalchemy; print('[OK] SQLAlchemy imported')"
python -c "import qdrant_client; print('[OK] Qdrant imported')"
python -c "import openai; print('[OK] OpenAI imported')"
python -c "from config import settings; print('[OK] Config loaded')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo If all packages show [OK], run: debug-backend.bat
echo.
pause
