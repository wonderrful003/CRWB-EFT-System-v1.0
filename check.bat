@echo off
chcp 65001 >nul
title CRWB EFT System - System Check (Python 3.9.0)
color 0F

echo ================================================
echo       CRWB EFT SYSTEM - SYSTEM CHECK
echo       PYTHON 3.9.0 VERIFICATION
echo ================================================
echo.

echo 🔍 1/7: Checking Python 3.9.0...
python --version
python -c "import sys; print(f'Architecture: {sys.platform} {8*sys.maxsize}-bit')"
echo.

echo 📁 2/7: Checking project structure...
if exist manage.py (echo ✅ manage.py) else (echo ❌ manage.py - CRITICAL)
if exist requirements.txt (echo ✅ requirements.txt) else (echo ❌ requirements.txt)
if exist eft_app\fixtures\all_data.json (echo ✅ Data file) else (echo ⚠ No data file)
if exist venv (echo ✅ Virtual environment) else (echo ❌ Virtual environment)
echo.

echo 💾 3/7: Checking database...
if exist db.sqlite3 (
    echo ✅ Database exists
    for /f %%i in ('python -c "import os; print(os.path.getsize(\"db.sqlite3\"))"') do set size=%%i
    set /a size_kb=size/1024
    echo   Size: !size_kb! KB
) else (
    echo ⚠ Database not found
)
echo.

echo 📦 4/7: Checking Python packages...
if exist venv (
    call venv\Scripts\activate.bat
    python -c "
try:
    import django
    print(f'✅ Django {django.__version__}')
except ImportError:
    print('❌ Django not installed')
"
    python -c "
try:
    import psycopg2
    print('✅ PostgreSQL support')
except ImportError:
    print('⚠ No PostgreSQL support')
"
) else (
    echo ⚠ Virtual environment not active
)
echo.

echo 👤 5/7: Checking users...
if exist db.sqlite3 (
    python manage.py shell -c "
try:
    from django.contrib.auth.models import User
    count = User.objects.count()
    print(f'✅ {count} user(s) in database')
    if count > 0:
        print('   Available users:')
        for user in User.objects.all()[:3]:
            print(f'   • {user.username} ({user.email})')
        if count > 3:
            print(f'   • ... and {count-3} more')
except Exception as e:
    print(f'❌ Could not check users: {e}')
" 2>nul
)
echo.

echo 📊 6/7: Checking system resources...
python -c "
import psutil
import os
mem = psutil.virtual_memory()
print(f'Memory: {mem.percent}%% used ({mem.available//1024//1024} MB free)')
disk = psutil.disk_usage('.')
print(f'Disk: {disk.percent}%% used ({disk.free//1024//1024} MB free)')
"
echo.

echo 🛠️ 7/7: Running Django system check...
python manage.py check

echo.
echo ================================================
echo 📋 SYSTEM STATUS SUMMARY
echo ================================================
echo • Python: Must be 3.9.0
echo • Virtual Environment: %cd%\venv
echo • Database: %cd%\db.sqlite3
echo • Data: eft_app\fixtures\all_data.json
echo • Ready: launch.bat or start.bat
echo ================================================
echo.
echo ✅ If all checks pass, run: start.bat
echo ⚠ If Python is not 3.9.0, download from:
echo    https://www.python.org/downloads/release/python-390/
echo.
pause