@echo off
chcp 65001 >nul
title CRWB EFT System - Reset
color 0C

echo ================================================
echo       CRWB EFT SYSTEM - RESET
echo ================================================
echo ⚠ WARNING: This will delete ALL data!
echo ================================================
echo.
echo Checking Python 3.9.0...
python --version | findstr /C:"Python 3.9.0" >nul
if errorlevel 1 (
    echo ❌ Python 3.9.0 required for reset!
    pause
    exit /b 1
)

echo What will be deleted:
echo • Virtual environment (venv/)
echo • Database (db.sqlite3)
echo • Database backups
echo • Python cache files
echo.
echo Your original data file will NOT be deleted.
echo.
choice /c YN /m "Continue with reset? (Y/N)"
if errorlevel 2 goto cancelled

echo.
echo 📦 1/4: Removing virtual environment...
if exist venv rmdir /s /q venv
echo ✅ Virtual environment removed
echo.

echo 🗑️ 2/4: Removing database files...
if exist db.sqlite3 del db.sqlite3
if exist db_backup_*.sqlite3 del db_backup_*.sqlite3
if exist backup_db_*.sqlite3 del backup_db_*.sqlite3
echo ✅ Database files removed
echo.

echo 🧹 3/4: Cleaning cache files...
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
del /s /q *.pyd 2>nul
if exist __pycache__ rmdir /s /q __pycache__
if exist eft_app\__pycache__ rmdir /s /q eft_app\__pycache__
if exist crwb_eft\__pycache__ rmdir /s /q crwb_eft\__pycache__
echo ✅ Cache cleaned
echo.

echo 📁 4/4: Creating fresh structure...
mkdir static 2>nul
mkdir media 2>nul
echo ✅ Fresh structure created
echo.

echo ================================================
echo ✅ RESET COMPLETE
echo ================================================
echo.
echo To setup fresh (requires Python 3.9.0):
echo 1. Run: launch.bat
echo 2. Or: setup.bat then start.bat
echo.
goto end

:cancelled
echo.
echo Reset cancelled.

:end
pause