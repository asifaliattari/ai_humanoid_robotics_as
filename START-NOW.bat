@echo off
color 0A
echo.
echo ================================================
echo STARTING BACKEND (Simple - No Database)
echo ================================================
echo.

cd backend
call venv\Scripts\activate.bat

echo [1] Generating embeddings (if needed)...
python -c "from services.qdrant_service import qdrant_service; collections = qdrant_service.client.get_collections(); print('Current collections:', [c.name for c in collections.collections])"

set /p has_embeddings="Does it show 'physical_ai_book' collection? (Y/N): "
if /i "%has_embeddings%"=="N" (
    echo.
    echo Generating embeddings...
    echo This costs ~$2-5 and takes 2-3 minutes
    python -m scripts.generate_embeddings
)

echo.
echo [2] Starting backend server...
echo.
echo ================================================
echo Backend running at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Test the chatbot:
echo 1. Open browser: http://localhost:8000/docs
echo 2. Try the /api/rag/book-qa endpoint
echo 3. Ask: "What is ROS 2?"
echo.
echo Press Ctrl+C to stop
echo ================================================
echo.

uvicorn main-simple:app --reload --host 0.0.0.0 --port 8000
