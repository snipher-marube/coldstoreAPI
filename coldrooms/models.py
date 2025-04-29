from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User

class ColdRoom(models.Model):
    APPROVAL_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cold_rooms')
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.PointField(geography=True)
    address = models.CharField(max_length=255)
    capacity_kg = models.PositiveIntegerField()
    price_per_kg_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    features = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

class ColdRoomImage(models.Model):
    cold_room = models.ForeignKey(ColdRoom, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='coldrooms/')
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']