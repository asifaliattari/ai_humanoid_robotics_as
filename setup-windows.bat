@echo off
echo ========================================
echo Physical AI Book - Automated Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please download Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/8] Python found:
python --version
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed!
    echo Please download Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo [2/8] Node.js found:
node --version
echo.

REM Create backend virtual environment
echo [3/8] Creating Python virtual environment...
cd backend
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate virtual environment and upgrade pip
echo [4/8] Upgrading pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
echo.

REM Install backend dependencies
echo [5/8] Installing backend dependencies...
echo This may take 3-5 minutes...
pip install fastapi==0.109.0
pip install "uvicorn[standard]==0.27.0"
pip install qdrant-client==1.7.3
pip install asyncpg==0.29.0
pip install sqlalchemy==2.0.25
pip install alembic==1.13.1
pip install openai==1.10.0
pip install tiktoken==0.5.2
pip install pydantic==2.5.3
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0
pip install httpx==0.26.0
pip install python-multipart==0.0.6
pip install "python-jose[cryptography]==3.3.0"
pip install "passlib[bcrypt]==1.7.4"
pip install python-json-logger==2.0.7

REM Try to install psycopg2-binary (optional)
echo Installing psycopg2-binary (may fail on Windows, that's OK)...
pip install psycopg2-binary --only-binary :all: 2>nul
if errorlevel 1 (
    echo psycopg2-binary skipped - using asyncpg only
) else (
    echo psycopg2-binary installed successfully!
)
echo.

REM Verify installation
echo [6/8] Verifying backend installation...
python -c "import fastapi, sqlalchemy, qdrant_client, openai; print('[SUCCESS] All core packages installed!')"
if errorlevel 1 (
    echo [ERROR] Some packages failed to install
    pause
    exit /b 1
)
echo.

REM Check if .env exists
echo [7/8] Checking configuration...
if exist .env (
    echo .env file found!
) else (
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit backend\.env with your API keys:
    echo   - QDRANT_URL and QDRANT_API_KEY
    echo   - DATABASE_URL
    echo   - OPENAI_API_KEY
    echo.
    echo Opening .env file for you to edit...
    timeout /t 2 >nul
    notepad .env
)
echo.

REM Install frontend dependencies
echo [8/8] Installing frontend dependencies...
cd ..
if exist node_modules (
    echo node_modules exists, skipping npm install...
    echo If you want to reinstall, delete node_modules folder first
) else (
    echo This may take 2-3 minutes...
    call npm install
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Make sure you've added your API keys to backend\.env
echo.
echo 2. Initialize database:
echo    cd backend
echo    venv\Scripts\activate
echo    alembic upgrade head
echo.
echo 3. Generate embeddings:
echo    python -m scripts.generate_embeddings
echo.
echo 4. Start backend (in one terminal):
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn main:app --reload
echo.
echo 5. Start frontend (in another terminal):
echo    npm start
echo.
echo Or use the quick start scripts:
echo    - start-backend.bat
echo    - start-frontend.bat
echo.
pause
