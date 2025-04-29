from django.urls import path
from knox import views as knox_views
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .views import RegisterAPI, LoginAPI, FacebookLogin, GoogleLogin

# Custom throttling classes
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'

urlpatterns = [
    # Authentication endpoints
    path('api/v1/auth/register/', 
        RegisterAPI.as_view(
            throttle_classes=[AnonRateThrottle]
        ), 
        name='auth-register'),
    
    path('api/v1/auth/login/', 
        LoginAPI.as_view(
            throttle_classes=[BurstRateThrottle]
        ), 
        name='auth-login'),
    
    # Social auth endpoints
    path('api/v1/auth/facebook/', 
        FacebookLogin.as_view(
            throttle_classes=[BurstRateThrottle]
        ), 
        name='fb_login'),
   
    
    path('api/v1/auth/google/', GoogleLogin.as_view(), name='google_login'),
    # Session management
    path('api/v1/auth/logout/', 
        knox_views.LogoutView.as_view(
            throttle_classes=[UserRateThrottle]
        ), 
        name='auth-logout'),
    
    path('api/v1/auth/logout-all/', 
        knox_views.LogoutAllView.as_view(
            throttle_classes=[SustainedRateThrottle]
        ), 
        name='auth-logout-all'),
]