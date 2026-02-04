@echo off
chcp 65001 >nul
title CRWB EFT System - Restore
color 0D

echo ================================================
echo       CRWB EFT SYSTEM - RESTORE
echo ================================================
echo.

echo Available backups:
echo.
dir backup_*.json /b
dir export_*.json /b 2>nul
echo.

set /p backup_file="Enter backup filename (or press Enter to cancel): "
if "%backup_file%"=="" goto cancelled

if not exist "%backup_file%" (
    echo ❌ Backup file not found: %backup_file%
    pause
    exit /b 1
)

echo.
echo ⚠ Restoring from: %backup_file%
echo This will overwrite current data!
echo.
choice /c YN /m "Continue? (Y/N)"
if errorlevel 2 goto cancelled

echo.
echo 📥 Copying backup file...
copy "%backup_file%" eft_app\fixtures\all_data.json /Y
echo ✅ Backup copied

echo 🔄 Resetting database...
if exist db.sqlite3 del db.sqlite3
python manage.py migrate --noinput
echo ✅ Database reset

echo 📂 Loading restored data...
python manage.py loaddata eft_app\fixtures\all_data.json
echo ✅ Data loaded

echo.
echo ================================================
echo ✅ RESTORE COMPLETE
echo ================================================
echo.
echo System restored from: %backup_file%
echo Run start.bat to start server
echo.
goto end

:cancelled
echo.
echo Restore cancelled.

:end
pause