from rest_framework import viewsets, permissions
from .serializers import ColdRoomSerializer, ColdRoomVerificationSerializer, ColdRoomsListSerializer
from .models import ColdRoom, ColdRoomVerification

class IsColdRoomOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class ColdRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ColdRoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsColdRoomOwner]

    def get_queryset(self):
        return ColdRoom.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically create the verification entry
        cold_room = serializer.save()
        ColdRoomVerification.objects.create(cold_room=cold_room)
    
class ColdRoomVerificationViewset(viewsets.ModelViewSet):
    serializer_class = ColdRoomVerificationSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return ColdRoomVerification.objects.select_related('cold_room', 'reviewed_by')

class ColdRoomListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ColdRoomsListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return ColdRoom.objects.filter(is_verified=True)
