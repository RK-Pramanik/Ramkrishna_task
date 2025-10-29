"""URL configuration for tms_project project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # Core pages
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    # App URLs
    path('tasks/', include('tasks.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Development-only media serving
if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)