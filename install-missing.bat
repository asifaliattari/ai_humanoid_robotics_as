@echo off
echo ========================================
echo Installing Missing Packages
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat

echo Installing SQLAlchemy...
pip install sqlalchemy==2.0.25

echo Installing Alembic...
pip install alembic==1.13.1

echo.
echo ========================================
echo Installation Complete
echo ========================================
echo.
echo Now run: debug-backend.bat
pause
