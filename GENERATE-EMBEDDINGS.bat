@echo off
echo ========================================
echo GENERATE EMBEDDINGS
echo ========================================
echo.
echo This will:
echo - Read all markdown files from docs/
echo - Generate embeddings using OpenAI
echo - Upload to Qdrant
echo.
echo Cost: ~$2-5 (one-time)
echo Time: 2-3 minutes
echo.
pause

cd backend
call venv\Scripts\activate.bat

echo.
echo [1] Checking current embeddings...
python check-embeddings.py
echo.

echo [2] Generating new embeddings...
python -m scripts.generate_embeddings

echo.
echo [3] Verifying embeddings...
python check-embeddings.py

echo.
echo ========================================
echo Done!
echo ========================================
pause
