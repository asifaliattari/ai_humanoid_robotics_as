@echo off
echo ========================================
echo FIXING AND GENERATING EMBEDDINGS
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat

echo [1] Upgrading Qdrant client...
pip install --upgrade qdrant-client
echo.

echo [2] Checking Qdrant connection...
python -c "from services.qdrant_service import qdrant_service; print('✅ Qdrant connected'); print('Collection:', qdrant_service.collection_name)"
echo.

echo [3] Generating embeddings...
echo This will cost ~$2-5 and take 2-3 minutes
echo.
pause

python -m scripts.generate_embeddings

echo.
echo ========================================
echo DONE! Now start the backend:
echo   START-NOW.bat
echo ========================================
pause
