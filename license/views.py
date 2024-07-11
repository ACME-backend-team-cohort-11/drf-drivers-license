# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import License
from .serializers import LicenseSerializer
from django.shortcuts import get_object_or_404
from datetime import date

class LicenseDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows retrieval of a specific license.
    """
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve the License object based on the license_id.
        """
        license_id = self.kwargs.get('license_id')  
        return get_object_or_404(License, licenseId=license_id)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific license.

        This endpoint returns the license details along with its current status (valid or expired).

        Parameters:
        - license_id (path): The unique identifier of the license

        Returns:
        - 200 OK: License details retrieved successfully
            {
                'licenseId': 'string',
                'issue_date': 'date',
                'expiry_date': 'date',
                'status': 'string'
            }
        - 404 Not Found: License does not exist
            {
                'error': 'License does not exist'
            }
        """
        try:
            instance = self.get_object()
        except License.DoesNotExist:
            return Response({'error': 'License does not exist'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()
        status_text = 'expired' if instance.expiry_date < today else 'valid'

        response_data = {
            'licenseId': instance.licenseId,
            'issue_date': instance.issue_date,
            'expiry_date': instance.expiry_date,
            'status': status_text,
        }
        return Response(response_data, status=status.HTTP_200_OK)
