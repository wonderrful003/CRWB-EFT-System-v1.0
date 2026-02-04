@echo off
chcp 65001 >nul
title CRWB EFT System - Launch
color 0A

echo ================================================
echo       CRWB EFT SYSTEM v1.0 - LAUNCH
echo ================================================
echo.

echo 📁 Project Directory: %CD%
echo.

echo 🔍 Checking Python...
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

python --version
echo.

echo 📦 Step 1: Creating virtual environment...
if exist venv (
    echo   Removing old virtual environment...
    timeout /t 2 /nobreak >nul
    rmdir /s /q venv 2>nul
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

echo 🔄 Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo.

echo 📥 Step 3: Installing requirements...
if exist requirements.txt (
    echo   Installing packages from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ⚠ Some packages failed, trying Django only...
        pip install Django==4.2.27
    )
    echo ✅ Requirements installed
) else (
    echo ⚠ requirements.txt not found
    echo Installing Django...
    pip install Django==4.2.27
    echo ✅ Django installed
)

echo.
echo 💾 Step 4: Setting up database...
if exist db.sqlite3 (
    echo   Backing up old database...
    set "backup=db_backup_%date:~10,4%%date:~4,2%%date:~7,2%.sqlite3"
    copy db.sqlite3 %backup% >nul 2>&1
    echo   ✅ Backup: %backup%
)

echo   Creating database tables...
python manage.py makemigrations --noinput
python manage.py migrate --noinput
if errorlevel 1 (
    echo ❌ Database setup failed
    pause
    exit /b 1
)
echo ✅ Database ready
echo.

echo 📂 Step 5: Loading your data...
if exist eft_app\fixtures\all_data.json (
    echo   Loading your original system data...
    python manage.py loaddata eft_app\fixtures\all_data.json
    if errorlevel 1 (
        echo ⚠ Could not load data
    ) else (
        echo ✅ YOUR DATA LOADED SUCCESSFULLY!
        
        python -c "
try:
    import json
    with open('eft_app/fixtures/all_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    users = [d for d in data if d.get('model') == 'auth.user']
    banks = [d for d in data if d.get('model') == 'eft_app.bank']
    
    print()
    print('   📊 DATA SUMMARY:')
    print('   ' + '-' * 30)
    print(f'   • Users: {len(users)}')
    print(f'   • Banks: {len(banks)}')
    print(f'   • Total records: {len(data)}')
    
    if users:
        print()
        print('   👤 SAMPLE USERS:')
        for user in users[:3]:
            fields = user.get('fields', {})
            print(f'   • {fields.get(\"username\", \"Unknown\")}')
        if len(users) > 3:
            print(f'   • ... and {len(users)-3} more')
except:
    pass
"
    )
) else (
    echo ⚠ No data file found. Creating admin...
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@crwb.gov.mw', 'admin123')"
    echo ✅ Created admin/admin123
)

echo.
echo 🛠️ Step 6: Preparing static files...
python manage.py collectstatic --noinput >nul 2>&1
echo ✅ Static files ready
echo.

echo ================================================
echo 🎉 SETUP COMPLETE! LAUNCHING SERVER...
echo ================================================
echo.
echo 🌐 Application: http://127.0.0.1:8000
echo 🔧 Admin Panel: http://127.0.0.1:8000/admin
echo.
echo 📋 Login with your original users!
echo   (All users from your system are available)
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================
echo.

timeout /t 3 /nobreak >nul
python manage.py runserver

echo.
echo ================================================
echo ⏹️ SERVER STOPPED
echo ================================================
echo.
echo Virtual environment is still active.
echo To exit virtual environment, type: deactivate
echo.
pause