from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="ColdStore API",
        default_version='v1',
        description="API for cold storage management",
        contact=openapi.Contact(email="dev@coldstore.com"),
        public=True,
    ),
        permission_classes=[permissions.AllowAny],
    )

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/v1/docs/', 
        schema_view.with_ui('swagger', cache_timeout=0), 
        name='api-docs'),
    
    # Health Check
    path('api/v1/health/', include('health_check.urls')),
    
    # Authentication
    path('', include(('users.urls', 'users'), namespace='auth')),
    
    # API Framework (Development Only)
    path('api/v1/auth/drf/', include('rest_framework.urls', namespace='rest_framework')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]