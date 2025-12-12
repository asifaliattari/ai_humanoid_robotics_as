@echo off
echo ========================================
echo Initialize Database
echo ========================================
echo.

cd backend

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [1/2] Running database migrations...
alembic upgrade head
if errorlevel 1 (
    echo [ERROR] Migration failed!
    echo Please check your DATABASE_URL in .env
    pause
    exit /b 1
)
echo.

echo [2/2] Generating embeddings...
echo This will:
echo  - Scan all markdown files in docs/
echo  - Generate embeddings using OpenAI
echo  - Upload to Qdrant
echo.
echo This costs about $2-5 (one-time) and takes 2-3 minutes
echo.
set /p continue="Continue? (Y/N): "
if /i "%continue%" neq "Y" (
    echo Skipping embeddings generation
    echo You can run this later with: generate-embeddings.bat
    pause
    exit /b 0
)

python -m scripts.generate_embeddings
if errorlevel 1 (
    echo [ERROR] Embedding generation failed!
    echo Please check your OPENAI_API_KEY and QDRANT credentials in .env
    pause
    exit /b 1
)

echo.
echo ========================================
echo Database initialized successfully!
echo ========================================
echo.
echo You can now start the servers:
echo  1. Run start-backend.bat (in one terminal)
echo  2. Run start-frontend.bat (in another terminal)
echo.
pause
