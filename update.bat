@echo off
chcp 65001 >nul
title CRWB EFT System - Update
color 0B

echo ================================================
echo       CRWB EFT SYSTEM - UPDATE
echo ================================================
echo.

if not exist venv (
    echo ❌ Virtual environment not found!
    echo Run setup.bat or launch.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 📦 Current package versions:
pip list --format=columns | findstr /i "django crispy"
echo.

echo 🔄 Updating packages...
pip install --upgrade -r requirements.txt
echo ✅ Packages updated
echo.

echo 📦 New package versions:
pip list --format=columns | findstr /i "django crispy"
echo.

echo 🔍 Checking for migrations...
python manage.py makemigrations --check --dry-run
echo.

echo 💾 Creating update backup...
set "timestamp=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%"
set "timestamp=%timestamp: =0%"
python manage.py dumpdata --indent 2 > update_backup_%timestamp%.json
echo ✅ Update backup: update_backup_%timestamp%.json
echo.

echo ================================================
echo ✅ UPDATE COMPLETE
echo ================================================
echo.
echo Run start.bat to start server with updates
echo.
pause