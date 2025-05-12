from django.contrib.gis import admin
#from django.contrib.gis.admin import OSMGeoAdmin
from .models import ColdRoom, ColdRoomVerification

@admin.register(ColdRoom)
class ColdRoomAdmin(admin.GISModelAdmin):
    list_display = ('name', 'owner', 'is_verified')
    list_filter = ('is_verified', 'temp_unit')
    search_fields = ('name', 'owner__email')
    default_lon = -1.1  # Default longitude for map center
    default_lat = 35.0  # Default latitude for map center
    default_zoom = 10

@admin.register(ColdRoomVerification)
class ColdRoomVerificationAdmin(admin.ModelAdmin):
    list_display = ('cold_room', 'status', 'submitted_at')
    list_filter = ('status',)
