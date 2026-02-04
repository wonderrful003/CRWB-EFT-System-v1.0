@echo off
chcp 65001 >nul
title CRWB EFT - Start Server
color 0C

echo ================================================
echo       CRWB EFT SYSTEM - START SERVER
echo ================================================
echo.

echo 🔍 Checking Python 3.9.0...
python --version | findstr /C:"Python 3.9.0" >nul
if errorlevel 1 (
    echo ❌ Python 3.9.0 not found!
    echo Download from: https://www.python.org/downloads/release/python-390/
    pause
    exit /b 1
)

if not exist venv (
    echo ❌ Virtual environment not found!
    echo Run setup.bat first.
    pause
    exit /b 1
)

if not exist db.sqlite3 (
    echo ⚠ Database not found!
    echo Run setup.bat first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ================================================
echo 🚀 STARTING SERVER...
echo ================================================
echo.
echo 🌐 Server: http://127.0.0.1:8000
echo 🔧 Admin: http://127.0.0.1:8000/admin
echo.
echo 📋 Login with your original users
echo.
echo Press Ctrl+C to stop
echo ================================================
echo.

python manage.py runserver

echo.
echo Server stopped.
echo Virtual environment still active.
echo Type 'deactivate' to exit.
pause