# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import License
from .serializers import LicenseSerializer
from django.shortcuts import get_object_or_404
from datetime import date

class LicenseDetailView(generics.RetrieveAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        license_id = self.kwargs.get('license_id')  
        return get_object_or_404(License, licenseId=license_id)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except License.DoesNotExist:
            return Response({'error': 'License does not exist'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        if instance.expiry_date < today:
            status_text = 'expired'
        else:
            status_text = 'valid'

        # Prepare the response data
        response_data = {
            'licenseId': instance.licenseId,
            'issue_date': instance.issue_date,
            'expiry_date': instance.expiry_date,
            'status': status_text,
        }

        return Response(response_data, status=status.HTTP_200_OK)
