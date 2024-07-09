# models.py
from django.db import models
from django.utils import timezone
from nationalId.models import NationalId
import uuid

class DriversLicenseApplication(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('New', 'New Application'),
        ('Renewal', 'Renewal Application'),
        ('Reissue', 'Reissue Application'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Ready for Printing', 'Ready for Printing'),
        ('Renewal Pending', 'Renewal Pending'),
        ('Renewal Processing', 'Renewal Processing'),
        ('Renewed', 'Renewed'),
        ('Reissue Pending', 'Reissue Pending'),
        ('Reissue Processing', 'Reissue Processing'),
        ('Reissued', 'Reissued'),
    ]

    application_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_motor_cycle = models.BooleanField(default=False)
    is_motor_vehicle = models.BooleanField(default=False)
    certificate_number = models.IntegerField()
    applied_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(NationalId, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES)
    license_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Additional fields for renewal and reissue
    previous_license_id = models.CharField(max_length=255, blank=True, null=True)
    renewal_applied_at = models.DateTimeField(blank=True, null=True)
    renewal_approved_at = models.DateTimeField(blank=True, null=True)
    reissue_applied_at = models.DateTimeField(blank=True, null=True)
    reissue_approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.application_id)

