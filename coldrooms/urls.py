from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColdRoomViewSet, ColdRoomVerificationViewset, ColdRoomListViewSet, ColdRoomSearchViewSet

router = DefaultRouter()
router.register(r'cold-rooms', ColdRoomViewSet, basename='coldroom')
router.register(r'verifications', ColdRoomVerificationViewset, basename='verification')
router.register(r'cold-rooms-list', ColdRoomListViewSet, basename='coldroom-list')
router.register(r'search', ColdRoomSearchViewSet, basename='coldroom-search')

urlpatterns = [
    path('', include(router.urls))
]