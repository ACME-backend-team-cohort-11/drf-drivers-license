from rest_framework import serializers
from .models import DriversLicenseApplication
from nationalId.models import NationalId

class DriversLicenseApplicationSerializer(serializers.ModelSerializer):
    nationalId = serializers.PrimaryKeyRelatedField(queryset=NationalId.objects.all())  # Adjust queryset as needed

    class Meta:
        model = DriversLicenseApplication
        fields = '__all__' 
#    def validate(self, data):
#       if not data.get('is_motor_cycle') and not data.get('is_motor_vehicle'):
#            raise serializers.ValidationError("At least one of is_motor_cycle or is_motor_vehicle must be True")
#        return data
