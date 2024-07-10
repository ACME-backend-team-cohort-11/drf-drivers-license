'''Accounts Serializers'''
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'date_joined')
