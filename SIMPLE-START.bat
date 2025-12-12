@echo off
echo ========================================
echo Simple Start - English Only Version
echo ========================================
echo.

echo [Step 1] Checking your Qdrant URL...
findstr "QDRANT_URL" backend\.env
echo.
echo Make sure QDRANT_URL starts with https://
echo Example: https://abc123-xyz.qdrant.io
echo.
pause

echo [Step 2] Installing required packages...
cd backend
call venv\Scripts\activate.bat

echo Installing core packages only...
pip install fastapi uvicorn qdrant-client openai pydantic pydantic-settings python-dotenv httpx python-multipart

echo.
echo [Step 3] Creating SQLite database...
python -c "from sqlalchemy import create_engine; engine = create_engine('sqlite:///database.db'); print('Database created!')"

echo.
echo [Step 4] Generating embeddings...
echo This will cost about $2-5 in OpenAI credits
set /p continue="Continue? (Y/N): "
if /i "%continue%" neq "Y" goto skip_embeddings

python -m scripts.generate_embeddings

:skip_embeddings

echo.
echo [Step 5] Starting backend...
echo Backend will be at: http://localhost:8000
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
