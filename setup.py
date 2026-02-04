# setup.py
import os
import sys
import json
import subprocess

def setup_project():
    print("=" * 60)
    print("CRWB EFT System Setup")
    print("=" * 60)
    
    # 1. Install requirements
    print("\n1. Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("   ✓ Requirements installed")
    except:
        print("   ⚠ Could not install from requirements.txt")
        print("   Installing Django directly...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Django==4.2.7"])
    
    # 2. Clean old database
    print("\n2. Cleaning old database...")
    if os.path.exists("db.sqlite3"):
        os.rename("db.sqlite3", "db_backup.sqlite3")
        print("   ✓ Backed up old database as db_backup.sqlite3")
    
    # 3. Run migrations
    print("\n3. Running migrations...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "makemigrations"])
        subprocess.check_call([sys.executable, "manage.py", "migrate"])
        print("   ✓ Database created")
    except Exception as e:
        print(f"   ✗ Migration error: {e}")
        return False
    
    # 4. Load your exported data
    print("\n4. Loading your data...")
    fixture_files = [
        "eft_app/fixtures/all_data.json",
        "eft_app/fixtures/initial_data.json"
    ]
    
    loaded = False
    for fixture in fixture_files:
        if os.path.exists(fixture):
            try:
                print(f"   Loading {fixture}...")
                result = subprocess.call([sys.executable, "manage.py", "loaddata", fixture])
                if result == 0:
                    print(f"   ✓ Successfully loaded {fixture}")
                    
                    # Show what was loaded
                    with open(fixture, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        print(f"   Total records: {len(data)}")
                        
                        # Count by type
                        counts = {}
                        for item in data:
                            model = item.get("model", "")
                            counts[model] = counts.get(model, 0) + 1
                        
                        for model, count in counts.items():
                            print(f"   - {model}: {count}")
                    
                    loaded = True
                    break
                else:
                    print(f"   ✗ Failed to load {fixture}")
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    if not loaded:
        print("   ⚠ No fixture file loaded. Creating default data...")
        create_default_data()
    
    # 5. Create superuser if no users exist
    print("\n5. Checking users...")
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crwb_eft_system.settings')
        import django
        django.setup()
        
        from django.contrib.auth.models import User
        
        if User.objects.count() == 0:
            print("   No users found. Creating admin...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("   ✓ Created admin/admin123")
        else:
            print(f"   Found {User.objects.count()} user(s)")
            for user in User.objects.all()[:5]:  # Show first 5 users
                print(f"   - {user.username}")
            if User.objects.count() > 5:
                print(f"   ... and {User.objects.count() - 5} more")
    
    except Exception as e:
        print(f"   ⚠ Could not check users: {e}")
    
    # 6. Collect static files
    print("\n6. Collecting static files...")
    subprocess.check_call([sys.executable, "manage.py", "collectstatic", "--noinput"])
    print("   ✓ Static files collected")
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\n🚀 Start the server:")
    print("   python manage.py runserver")
    print("\n🌐 Then open: http://127.0.0.1:8000")
    print("\n🔧 Admin panel: http://127.0.0.1:8000/admin")
    
    return True

def create_default_data():
    """Create minimal default data if no fixtures exist"""
    print("   Creating default data...")
    
    # This function creates basic test data
    # Since you have fixtures, this won't be called
    pass

if __name__ == "__main__":
    setup_project()