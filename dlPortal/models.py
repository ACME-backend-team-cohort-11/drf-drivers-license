"""Portal app models."""
from django.db import models
from django.contrib.auth.models import Group, Permission, AbstractUser
from django.utils import timezone
from nationalId.models import NationalId

class CustomUser(AbstractUser):
    id = models.OneToOneField(NationalId, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:  # if creating new instance
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CustomUser, self).save(*args, **kwargs)
