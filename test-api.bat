@echo off
echo ========================================
echo Testing API Endpoints
echo ========================================
echo.

echo Make sure backend is running first!
echo (Run start-backend.bat in another window)
echo.
pause

echo.
echo [1] Testing health endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo [2] Testing supported languages...
curl -s http://localhost:8000/api/translation/supported-languages
echo.
echo.

echo [3] Testing RAG book-qa (this will fail if embeddings not generated)...
curl -s -X POST http://localhost:8000/api/rag/book-qa ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What is ROS 2?\"}"
echo.
echo.

echo ========================================
echo API Tests Complete
echo ========================================
pause
