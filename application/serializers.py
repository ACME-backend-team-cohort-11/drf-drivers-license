from rest_framework import serializers
from .models import DriversLicenseApplication

class DriversLicenseApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriversLicenseApplication
        fields = '__all__'
