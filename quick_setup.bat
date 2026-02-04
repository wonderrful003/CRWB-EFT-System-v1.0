@echo off
echo CRWB EFT Quick Setup (Python 3.9.0)
echo ===================================
echo.

echo Checking Python 3.9.0...
python --version | findstr /C:"Python 3.9.0" >nul
if errorlevel 1 (
    echo ERROR: Python 3.9.0 required!
    exit /b 1
)

if exist venv rmdir /s /q venv
python -m venv venv
call venv\Scripts\activate.bat
pip install Django==4.2.27
if exist db.sqlite3 del db.sqlite3
python manage.py makemigrations
python manage.py migrate
if exist eft_app\fixtures\all_data.json python manage.py loaddata eft_app\fixtures\all_data.json
echo.
echo ✅ Quick setup complete!
echo Run: start.bat
pause