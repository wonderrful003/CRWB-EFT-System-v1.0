import os
import django
from django.template.loader import render_to_string
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crwb_eft.settings')
django.setup()

# Create test context
context = {
    'stats': {
        'users_count': 1,
        'active_users_count': 1,
        'banks_count': 0,
        'suppliers_count': 0,
        'zones_count': 0,
        'schemes_count': 0,
        'debit_accounts_count': 0,
    },
    'system_info': {
        'server_time': '2024-01-29',
        'python_version': '3.x',
        'django_version': '4.2.7',
        'os': 'Test',
        'memory_percent': 30,
        'disk_percent': 45,
        'cpu_percent': 25,
        'uptime': '1d 2h 30m',
    },
    'recent_activities': [],
    'user': User.objects.first(),
}

try:
    html = render_to_string('admin/dashboard.html', context)
    print("✅ Template rendering: OK")
    print(f"✅ Template length: {len(html)} characters")
except Exception as e:
    print(f"❌ Template error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()