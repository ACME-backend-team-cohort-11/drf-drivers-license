from django.db import models

class NationalId(models.Model):
    idNo = models.IntegerField(primary_key=True, null=False)
    firstName = models.CharField(max_length=255, null=False)
    middleName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    DOB = models.DateField(null=False)
    Sex = models.CharField(max_length=10, null=True, blank=True)
    Passport = models.ImageField(upload_to='passports/', null=True, blank=True)
    issuedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName or ''}"
