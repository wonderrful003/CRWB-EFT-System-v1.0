# diagnostic.py
# Save this file in C:\Users\dell\Desktop\crwb_eft_system\
# Run it with: python diagnostic.py

import os
import sys

print("=" * 60)
print("DJANGO PROJECT STRUCTURE DIAGNOSTIC")
print("=" * 60)

# Get current directory
current_dir = os.getcwd()
print(f"\n1. Current Directory: {current_dir}")

# Check for manage.py
if os.path.exists('manage.py'):
    print("   ✓ manage.py found")
    
    # Read manage.py to find project name
    with open('manage.py', 'r') as f:
        content = f.read()
        for line in content.split('\n'):
            if 'DJANGO_SETTINGS_MODULE' in line:
                print(f"   → {line.strip()}")
                # Extract project name
                if "'" in line or '"' in line:
                    parts = line.split("'") if "'" in line else line.split('"')
                    if len(parts) >= 2:
                        settings_module = parts[1]
                        project_name = settings_module.split('.')[0]
                        print(f"   → Detected project name: {project_name}")
else:
    print("   ✗ manage.py NOT found - Are you in the right directory?")

# List all directories (excluding venv and __pycache__)
print("\n2. Directory Structure:")
for item in os.listdir('.'):
    if os.path.isdir(item) and item not in ['venv', '__pycache__', '.git', 'staticfiles']:
        print(f"   📁 {item}/")
        
        # Check if this folder has settings.py
        settings_path = os.path.join(item, 'settings.py')
        if os.path.exists(settings_path):
            print(f"      ✓ Contains settings.py ← THIS IS YOUR PROJECT FOLDER!")
        
        # Check if this folder has urls.py
        urls_path = os.path.join(item, 'urls.py')
        if os.path.exists(urls_path):
            print(f"      ✓ Contains urls.py")
        
        # Check if this folder has wsgi.py
        wsgi_path = os.path.join(item, 'wsgi.py')
        if os.path.exists(wsgi_path):
            print(f"      ✓ Contains wsgi.py")

# Check for settings.py in root
if os.path.exists('settings.py'):
    print("\n   ⚠ WARNING: settings.py found in ROOT directory!")
    print("   This is unusual. Your project has a flat structure.")

# Find all settings.py files
print("\n3. Searching for settings.py files:")
for root, dirs, files in os.walk('.'):
    # Skip venv
    if 'venv' in root or '__pycache__' in root:
        continue
    if 'settings.py' in files:
        full_path = os.path.join(root, 'settings.py')
        print(f"   → Found: {full_path}")

# Find all urls.py files
print("\n4. Searching for urls.py files:")
for root, dirs, files in os.walk('.'):
    if 'venv' in root or '__pycache__' in root:
        continue
    if 'urls.py' in files:
        full_path = os.path.join(root, 'urls.py')
        print(f"   → Found: {full_path}")

# Check templates directory
print("\n5. Templates Directory:")
if os.path.exists('templates'):
    print("   ✓ templates/ folder exists in root")
    if os.path.exists('templates/registration'):
        print("   ✓ templates/registration/ exists")
        if os.path.exists('templates/registration/login.html'):
            print("   ✓ templates/registration/login.html exists")
        else:
            print("   ✗ templates/registration/login.html NOT FOUND")
    else:
        print("   ✗ templates/registration/ NOT FOUND")
else:
    print("   ✗ templates/ folder NOT FOUND in root")

# Check for templates in eft_app
if os.path.exists('eft_app/templates'):
    print("   ✓ eft_app/templates/ folder exists")
    if os.path.exists('eft_app/templates/registration'):
        print("   ✓ eft_app/templates/registration/ exists")
        if os.path.exists('eft_app/templates/registration/login.html'):
            print("   ✓ eft_app/templates/registration/login.html exists")

# Check static directory
print("\n6. Static Files:")
if os.path.exists('static'):
    print("   ✓ static/ folder exists")
else:
    print("   ✗ static/ folder NOT FOUND (create it)")

print("\n" + "=" * 60)
print("RECOMMENDATIONS:")
print("=" * 60)

# Try to determine the correct configuration
if os.path.exists('manage.py'):
    with open('manage.py', 'r') as f:
        content = f.read()
        for line in content.split('\n'):
            if 'DJANGO_SETTINGS_MODULE' in line and ("'" in line or '"' in line):
                parts = line.split("'") if "'" in line else line.split('"')
                if len(parts) >= 2:
                    settings_module = parts[1]
                    project_name = settings_module.split('.')[0]
                    
                    print(f"\n✓ Your project name is: {project_name}")
                    print(f"\nIn your settings.py, you should have:")
                    print(f"   ROOT_URLCONF = '{project_name}.urls'")
                    print(f"   WSGI_APPLICATION = '{project_name}.wsgi.application'")
                    
                    # Check if this folder exists
                    if os.path.exists(project_name):
                        print(f"\n✓ Folder '{project_name}/' exists")
                        if os.path.exists(f'{project_name}/settings.py'):
                            print(f"✓ {project_name}/settings.py exists")
                        else:
                            print(f"✗ {project_name}/settings.py NOT FOUND!")
                            print(f"\n⚠ PROBLEM DETECTED:")
                            print(f"   manage.py expects settings at: {project_name}.settings")
                            print(f"   But the file doesn't exist!")
                    else:
                        print(f"\n✗ PROBLEM: Folder '{project_name}/' does NOT exist!")
                        print(f"   But manage.py is looking for it!")

print("\n" + "=" * 60)
print("Next steps: Check the output above and fix your settings.py")
print("=" * 60)