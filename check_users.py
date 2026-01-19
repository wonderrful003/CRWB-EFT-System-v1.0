# setup_users.py
# Save this in: C:\Users\dell\Desktop\crwb_eft_system\
# Run with: python manage.py shell < setup_users.py

from django.contrib.auth.models import User, Group
from eft_app.permissions import create_groups_and_permissions

print("=" * 60)
print("CRWB EFT SYSTEM - USER SETUP")
print("=" * 60)

# Step 1: Create groups and permissions
print("\n1. Setting up groups and permissions...")
try:
    create_groups_and_permissions()
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("   Continuing anyway...")

# Step 2: Create test users
print("\n2. Creating test users...")

users_to_create = [
    {
        'username': 'sysadmin',
        'password': 'Test@1234',
        'first_name': 'System',
        'last_name': 'Admin',
        'email': 'sysadmin@crwb.com',
        'group': 'System Admin'
    },
    {
        'username': 'accounts',
        'password': 'Test@1234',
        'first_name': 'Accounts',
        'last_name': 'User',
        'email': 'accounts@crwb.com',
        'group': 'Accounts Personnel'
    },
    {
        'username': 'authorizer',
        'password': 'Test@1234',
        'first_name': 'Auth',
        'last_name': 'User',
        'email': 'authorizer@crwb.com',
        'group': 'Authorizer'
    }
]

for user_data in users_to_create:
    username = user_data['username']
    group_name = user_data.pop('group')
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"   ⚠ User '{username}' already exists - skipping")
        user = User.objects.get(username=username)
        # Make sure they have the right group
        try:
            group = Group.objects.get(name=group_name)
            if not user.groups.filter(name=group_name).exists():
                user.groups.add(group)
                print(f"      → Added to group: {group_name}")
        except Group.DoesNotExist:
            print(f"      ✗ Group '{group_name}' not found!")
    else:
        # Create new user
        try:
            user = User.objects.create_user(**user_data)
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            print(f"   ✓ Created user: {username} ({group_name})")
        except Exception as e:
            print(f"   ✗ Error creating {username}: {e}")

# Step 3: Summary
print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("=" * 60)
print("\nTest Login Credentials:")
print("-" * 60)
print("System Admin:")
print("  Username: sysadmin")
print("  Password: Test@1234")
print("\nAccounts Personnel:")
print("  Username: accounts")
print("  Password: Test@1234")
print("\nAuthorizer:")
print("  Username: authorizer")
print("  Password: Test@1234")
print("-" * 60)
print("\nYou can now run: python manage.py runserver")
print("Then visit: http://127.0.0.1:8000/")
print("=" * 60)