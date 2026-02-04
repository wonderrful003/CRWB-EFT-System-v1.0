@echo off
echo ========================================
echo CRWB EFT System - Setup Only
echo ========================================
echo.

echo This will set up the project but NOT run the server.
echo After setup, you'll need to manually run the server.
echo.
choice /c YN /m "Continue with setup? (Y/N)"
if errorlevel 2 goto :eof

echo.
echo 📁 Current directory: %CD%
echo.

echo 1. Creating virtual environment...
if exist venv rmdir /s /q venv 2>nul
python -m venv venv
call venv\Scripts\activate.bat

echo 2. Installing requirements...
pip install -r requirements.txt

echo 3. Setting up database...
if exist db.sqlite3 del db.sqlite3
python manage.py makemigrations
python manage.py migrate

echo 4. Loading your data...
if exist eft_app\fixtures\all_data.json (
    python manage.py loaddata eft_app\fixtures\all_data.json
    echo ✅ Your original data loaded!
) else (
    echo ⚠ No data file. Creating admin...
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
)

echo.
echo ========================================
echo ✅ SETUP COMPLETE!
echo ========================================
echo.
echo Virtual environment is ACTIVE.
echo.
echo To start server:
echo   python manage.py runserver
echo.
echo To deactivate later:
echo   deactivate
echo.
pause