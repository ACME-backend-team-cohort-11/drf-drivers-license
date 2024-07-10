from django.db import models
from django.utils import timezone
from nationalId.models import NationalId
import uuid



class License(models.Model):
    IdNo = models.ForeignKey(NationalId,on_delete=models.CASCADE)
    licenseId = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    passport_photo = models.ImageField(upload_to='passport_photos/', null=False, blank=False)

    def __str__(self):
        return self.licenseId
    
    # def is_fake(self):
         
    #     if self.issued_date > date.today():
    #         return True
    #     if 'FAKE' in self.license_number.upper():
    #         return True
    #     return False

    # @classmethod
    # def check_license_number(cls, license_number):
    #     try:
    #         cls.objects.get(license_number=license_number)
    #         return False  
    #     except cls.DoesNotExist:
    #         return True  
