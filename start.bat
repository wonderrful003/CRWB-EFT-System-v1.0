@echo off
echo ========================================
echo CRWB EFT System - Start Server
echo ========================================
echo.

echo Checking if virtual environment exists...
if not exist venv (
    echo ❌ Virtual environment not found!
    echo Run setup.bat first.
    pause
    goto :eof
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ========================================
echo 🚀 STARTING SERVER...
echo ========================================
echo.
echo Project: %CD%
echo Server: http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo.
echo Press Ctrl+C to stop
echo.

python manage.py runserver

echo.
echo Server stopped.
echo Virtual environment still active.
echo Type 'deactivate' to exit.
pause