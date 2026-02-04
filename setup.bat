@echo off
chcp 65001 >nul
title CRWB EFT - Setup (Python 3.9.0 Required)
color 0B

echo ================================================
echo       CRWB EFT SYSTEM - SETUP
echo       REQUIRES PYTHON 3.9.0
echo ================================================
echo.

echo This script sets up the project but NOT start the server.
echo Run 'start.bat' after this to start the server.
echo.
echo 🔍 Verifying Python 3.9.0...
python --version | findstr /C:"Python 3.9.0" >nul
if errorlevel 1 (
    echo ❌ Python 3.9.0 not found!
    echo Download from: https://www.python.org/downloads/release/python-390/
    pause
    exit /b 1
)

echo ✅ Python 3.9.0 confirmed
echo.
pause

echo 📦 Creating virtual environment...
if exist venv rmdir /s /q venv 2>nul
python -m venv venv
call venv\Scripts\activate.bat

echo 📥 Installing requirements for Python 3.9.0...
pip install -r requirements.txt

echo 💾 Setting up database...
if exist db.sqlite3 del db.sqlite3
python manage.py makemigrations
python manage.py migrate

echo 📂 Loading your data...
if exist eft_app\fixtures\all_data.json (
    python manage.py loaddata eft_app\fixtures\all_data.json
    echo ✅ Your data loaded!
) else (
    echo Creating admin user...
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
    echo ✅ Created admin/admin123
)

echo.
echo ================================================
echo ✅ SETUP COMPLETE
echo ================================================
echo.
echo Next steps:
echo 1. To start server: start.bat
echo 2. Open: http://127.0.0.1:8000
echo 3. Login with your original users
echo.
pause