import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crwb_eft.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User

try:
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Database connection: OK")
    
    # Test basic query
    count = User.objects.count()
    print(f"✅ User query: OK ({count} users)")
    
except Exception as e:
    print(f"❌ Database error: {e}")