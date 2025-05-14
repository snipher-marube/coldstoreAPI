from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
    path('api/v1/health/', include('health_check.urls')),
    path('', include(('users.urls', 'users'), namespace='auth')),
    path('api/v1/auth/drf/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Keep these for allauth/dj-rest-auth compatibility
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/social/', include('allauth.socialaccount.urls')),

    # cold room urls
    path('api/v1/', include('coldrooms.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]