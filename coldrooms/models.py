from django.contrib.gis.db import models
from django.contrib.postgres.indexes import GistIndex
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from users.models import User

class ColdRoom(models.Model):
    class TemperatureUnit(models.TextChoices):
        CELSIUS = 'C', _('Celsius')
        FAHRENHEIT = 'F', _('Fahrenheit')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='cold_room', 
                              limit_choices_to={'user_type': User.UserType.COLD_ROOM_OWNER})
    name = models.CharField(_('Cold Room Name'), max_length=255)
    location = models.PointField(_('Geographic Location'), srid=4326, 
                                 help_text=_('Use map widget to select location'))
    capacity = models.PositiveIntegerField(_('Storage Capacity'), 
                                           help_text=_('Total storage units (boxes/pallets) available'))
    temp_min = models.DecimalField(_('Minimum Temperature'), max_digits=5, decimal_places=2)
    temp_max = models.DecimalField(_('Maximum Temperature'), max_digits=5, decimal_places=2)
    temp_unit = models.CharField(_('Temperature Unit'), max_length=10,
                                 choices=TemperatureUnit.choices, default=TemperatureUnit.CELSIUS)
    availability_schedule = JSONField(_('Availability Calender'), default=dict, blank=True, 
                                      help_text=_('JSON structure defining available time slots'))
    is_verified = models.BooleanField(_('Verified Status'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cold Room')
        verbose_name_plural = _('Cold Rooms')
        indexes = [
            # Regular B-tree index for verified status and capacity
            models.Index(
                fields=['is_verified', 'capacity'],
                name='coldroom_verified_capacity_idx'
            ),
            # Spatial GiST index for location
            GistIndex(
                fields=['location'],
                name='coldroom_location_gist'
            ),
            
        ]

    def __str__(self):
        return f"{self.name} - ({self.owner.get_full_name()})"
    
class ColdRoomVerification(models.Model):
    class ColdRoomVerificationStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
    
    cold_room = models.OneToOneField(ColdRoom, on_delete=models.CASCADE, related_name='verification')
    status = models.CharField(_('Verification Status'), max_length=10, 
                              choices=ColdRoomVerificationStatus.choices,
                              default=ColdRoomVerificationStatus.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True, limit_choices_to={'is_staff': True})
    Verification_notes = models.TextField(_('Admin Notes'), blank=True)
    documentation = models.FileField(_('Verification Documents'), upload_to='coldroom/verifications/',
                                     blank=True, null=True)
    
    class Meta:
        verbose_name = _('Cold Room Verification')
        verbose_name_plural = _('Cold Room Verifications')

    def __str__(self):
        return f"Verification for {self.cold_room.name}- {self.status}"