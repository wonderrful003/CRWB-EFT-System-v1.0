# crwb_eft/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Django Built-in Admin (for superusers)
    path('admin/', admin.site.urls, name='django_admin'),
    
    # Your Custom System Admin (for System Admin group users)
    # This is already included from eft_app.urls
    path('', include('eft_app.urls')),
    
    # Optional: Redirect from old django-admin/ URL
    path('django-admin/', RedirectView.as_view(pattern_name='django_admin')),
]

# Add static and media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)