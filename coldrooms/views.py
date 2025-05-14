from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
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
    
# search the cold room by radius km
class ColdRoomSearchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ColdRoomsListSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']

    def get_queryset(self):
        queryset = ColdRoom.objects.filter(is_verified=True)

        # extract and validate parameters
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius', 5) # Default 5 km

        if not (lat and lon):
            return queryset.none()
        

        try:
            lat = float(lat)
            lon = float(lon)
            radius = float(radius)
        except (TypeError, ValueError):
            return queryset.none()
        
        # create point and filter within radius
        user_location = Point(lon, lat, srid=4326)
        return queryset.annotate(
            distance=Distance('location', user_location)
        ).filter(
            location__distance_lte=(user_location, D(km=radius))
        ).order_by('distance')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            radius = request.query_params.get('radius', 5)
            return Response ({
                'detail': f"No verified cold rooms found within {radius} km radius",
                "suggestions": [
                    "Try increasing the search radius",
                    "Check your location parameters",
                    'Verify cold room availability in neighbouring areas'
                ]
            }, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data,
            "search_parameters": {
                'latitude': request.query_params.get('lat'),
                'longitude': request.query_params.get('lon'),
                'radius_km': float(request.query_params.get('radius', 5)),
                'unit': 'Kilometers'
            }
        })