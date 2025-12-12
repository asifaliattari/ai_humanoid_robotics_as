@echo off
color 0A
echo.
echo     ================================================
echo     PHYSICAL AI BOOK - AUTOMATED SETUP
echo     ================================================
echo.
echo     This will:
echo     1. Check your API keys
echo     2. Install all packages
echo     3. Create database
echo     4. Generate embeddings ($2-5 cost)
echo     5. Start the backend
echo.
echo     ================================================
echo.
pause

cd backend

REM Step 1: Check Qdrant URL
echo.
echo [1/6] Checking Qdrant URL...
findstr /C:"your-cluster.qdrant.io" .env >nul
if %errorlevel%==0 (
    echo.
    echo [ERROR] You need to set your REAL Qdrant URL!
    echo.
    echo Open: backend\.env
    echo Find: QDRANT_URL="https://your-cluster.qdrant.io"
    echo Replace with your actual cluster URL from https://cloud.qdrant.io/
    echo.
    pause
    exit /b 1
)
echo [OK] Qdrant URL looks configured
echo.

REM Step 2: Activate venv
echo [2/6] Activating virtual environment...
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Run: fresh-install.bat first
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Step 3: Install packages
echo [3/6] Installing required packages...
echo This may take 2-3 minutes...
echo.
pip install --quiet fastapi==0.109.0
pip install --quiet "uvicorn[standard]==0.27.0"
pip install --quiet qdrant-client==1.7.3
pip install --quiet openai==1.10.0
pip install --quiet pydantic==2.5.3
pip install --quiet pydantic-settings==2.1.0
pip install --quiet python-dotenv==1.0.0
pip install --quiet httpx==0.26.0
pip install --quiet python-multipart==0.0.6

echo [OK] Core packages installed
echo.

REM Step 4: Verify installation
echo [4/6] Verifying packages...
python -c "import fastapi; import qdrant_client; import openai; print('[OK] All packages working')" 2>nul
if errorlevel 1 (
    echo [ERROR] Package verification failed
    pause
    exit /b 1
)
echo.

REM Step 5: Generate embeddings
echo [5/6] Generating embeddings...
echo.
echo This will:
echo - Scan all markdown files in docs/
echo - Generate embeddings using OpenAI (~$2-5)
echo - Upload to Qdrant
echo - Takes 2-3 minutes
echo.
set /p continue="Continue with embedding generation? (Y/N): "
if /i "%continue%" neq "Y" (
    echo.
    echo Skipping embeddings. You can run this later:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   python -m scripts.generate_embeddings
    echo.
    goto start_server
)

python -m scripts.generate_embeddings
if errorlevel 1 (
    echo.
    echo [ERROR] Embedding generation failed!
    echo Check your OPENAI_API_KEY and QDRANT credentials in .env
    pause
    exit /b 1
)
echo.
echo [OK] Embeddings generated successfully!
echo.

:start_server
REM Step 6: Start server
echo [6/6] Starting backend server...
echo.
echo ================================================
echo Backend is starting at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo To test the chatbot:
echo 1. Open another terminal
echo 2. Run: npm start
echo 3. Go to http://localhost:3000
echo 4. Click the chat button
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
