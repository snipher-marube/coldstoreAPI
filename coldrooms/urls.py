from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColdRoomViewSet, ColdRoomVerificationViewset

router = DefaultRouter()
router.register(r'cold-rooms', ColdRoomViewSet, basename='coldroom')
router.register(r'verifications', ColdRoomVerificationViewset, basename='verification')

urlpatterns = [
    path('', include(router.urls))
]