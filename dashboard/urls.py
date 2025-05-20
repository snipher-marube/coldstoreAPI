from django.urls import path
from .views import (
    ColdRoomDashboardView,
    ColdRoomCreateView,
    ColdRoomUpdateView,
    ColdRoomDetailView,
    VerificationRequestView
)

urlpatterns = [
    path('dashboard/', ColdRoomDashboardView.as_view(), name='coldroom-dashboard'),
    path('new/', ColdRoomCreateView.as_view(), name='coldroom-create'),
    path('<int:pk>/', ColdRoomDetailView.as_view(), name='coldroom-detail'),
    path('<int:pk>/edit/', ColdRoomUpdateView.as_view(), name='coldroom-update'),
    path('<int:pk>/verify/', VerificationRequestView.as_view(), name='coldroom-verify'),
]