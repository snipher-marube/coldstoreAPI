from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import ColdRoom, ColdRoomVerification


class ColdRoomSerializer(GeoFeatureModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    owner_email = serializers.EmailField(source='owner.email', write_only=True)

    class Meta:
        model = ColdRoom
        geo_field = 'location'
        fields = ['id', 'name', 'location', 'latitude', 'longitude',
                  'capacity', 'temp_min','temp_max', 'temp_unit',
                  'availability_schedule', 'is_verified', 'owner_email',
                  'created_at', 'updated_at']
        read_only_fields = ['is_verified', 'creatd_at', 'updated_at']

    def create(self, validated_data):
        # extract coordinates and convert them to point
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        validated_data['location'] = Point(latitude, longitude, srid=4326)

        # set owner for request user
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
class ColdRoomVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColdRoomVerification
        fields = ['id', 'cold_room', 'status', 'submitted_at',
                  'reviewed_at', 'reviewed_by', 'submitted_at', 'verification_notes', 'documentation']
        read_only_fields = ['reviewed_at', 'submitted_at', 'reviewed_by']


