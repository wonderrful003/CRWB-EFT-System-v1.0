@echo off
chcp 65001 >nul
title CRWB EFT System v1.0 - Launcher (Python 3.9.0 Required)
color 0A

echo ================================================
echo       CRWB EFT SYSTEM v1.0 - LAUNCHER
echo       REQUIRES PYTHON 3.9.0
echo ================================================
echo.

echo 📁 Project Directory: %CD%
echo.

echo 🔍 Checking Python 3.9.0 installation...
python --version > python_version.txt 2>&1
findstr /C:"Python 3.9.0" python_version.txt >nul
if errorlevel 1 (
    echo ❌ ERROR: Python 3.9.0 not found!
    echo.
    echo Current Python version:
    type python_version.txt
    echo.
    echo ⚠️ This system requires Python 3.9.0 exactly!
    echo Download from: https://www.python.org/downloads/release/python-390/
    echo.
    echo Make sure to:
    echo 1. Download Python 3.9.0
    echo 2. Install with "Add Python to PATH" checked
    echo 3. Restart Command Prompt
    echo.
    del python_version.txt
    pause
    exit /b 1
)

del python_version.txt
echo ✅ Python 3.9.0 detected
echo.

echo 📦 Step 1: Creating virtual environment...
if exist venv (
    echo   Removing old environment...
    timeout /t 2 /nobreak >nul
    rmdir /s /q venv 2>nul
)

python -m venv venv
call venv\Scripts\activate.bat

echo 📥 Step 2: Installing requirements for Python 3.9.0...
pip install -r requirements.txt

echo 💾 Step 3: Setting up database...
if exist db.sqlite3 (
    echo   Backing up old database...
    set "timestamp=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%"
    set "timestamp=%timestamp: =0%"
    copy db.sqlite3 backup_db_%timestamp%.sqlite3 >nul 2>&1
)

python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo 📂 Step 4: Loading your data...
if exist eft_app\fixtures\all_data.json (
    python manage.py loaddata eft_app\fixtures\all_data.json
    echo ✅ Your original data loaded (6 users, 6 banks, etc.)
) else (
    echo ⚠ Creating admin user...
    python manage.py createsuperuser --noinput --username admin --email admin@crwb.gov.mw
    echo ✅ Created admin/admin123
)

echo 🎨 Step 5: Collecting static files...
python manage.py collectstatic --noinput >nul 2>&1

echo.
echo ================================================
echo 🎉 SETUP COMPLETE! LAUNCHING SERVER...
echo ================================================
echo.
echo 🌐 Application: http://127.0.0.1:8000
echo 🔧 Admin Panel: http://127.0.0.1:8000/admin
echo.
echo 📋 Login with your original users
echo Press Ctrl+C to stop server
echo.
echo ================================================
echo.

timeout /t 3 /nobreak >nul
python manage.py runserver

echo.
echo ================================================
echo ⏹️ Server stopped
echo ================================================
echo.
echo Commands:
echo • deactivate - Exit virtual environment
echo • start.bat  - Start server again
echo • check.bat  - Run system diagnostics
echo.
pause