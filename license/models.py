from django.db import models
from django.utils import timezone
from nationalId.models import NationalId

class License(models.Model):
    IdNo = models.ForeignKey(NationalId,on_delete=models.CASCADE)
    licenseId = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    passport_photo = models.ImageField(upload_to='passport_photos/', null=False, blank=False)

    def __str__(self):
        return self.licenseId
