@echo off
chcp 65001 >nul
title CRWB EFT System - Backup
color 0E

echo ================================================
echo       CRWB EFT SYSTEM - BACKUP
echo ================================================
echo.

set "timestamp=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%"
set "timestamp=%timestamp: =0%"

echo 📅 Creating backup: %timestamp%
echo.

echo 📦 1/4: Backing up database...
if exist db.sqlite3 (
    copy db.sqlite3 backup_db_%timestamp%.sqlite3
    echo ✅ Database backup: backup_db_%timestamp%.sqlite3
) else (
    echo ⚠ No database found
)
echo.

echo 📄 2/4: Backing up data file...
if exist eft_app\fixtures\all_data.json (
    copy eft_app\fixtures\all_data.json backup_data_%timestamp%.json
    echo ✅ Data backup: backup_data_%timestamp%.json
) else (
    echo ⚠ No data file found
)
echo.

echo 💾 3/4: Creating export backup...
python manage.py dumpdata --indent 2 > export_%timestamp%.json 2>nul
if exist export_%timestamp%.json (
    echo ✅ Export backup: export_%timestamp%.json
) else (
    echo ⚠ Could not create export
)
echo.

echo 📁 4/4: Listing all backups...
dir backup_*.* /b
dir export_*.json /b 2>nul
echo.

echo ================================================
echo ✅ BACKUP COMPLETE
echo ================================================
echo.
echo Backups created with timestamp: %timestamp%
echo.
echo To restore from backup:
echo • Copy backup file to eft_app/fixtures/all_data.json
echo • Run: launch.bat
echo.
pause