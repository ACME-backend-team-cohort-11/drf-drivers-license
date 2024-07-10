# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import License
from .serializers import LicenseSerializer
from django.shortcuts import get_object_or_404
from datetime import date

class LicenseValidityView(generics.RetrieveAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     today = date.today()
    #     is_valid = instance.expiry_date >= today
    #     return Response({'valid': is_valid})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        today = date.today()
        
        if instance.expiry_date < today:
            status_text = 'expired'
        else:
            status_text = 'valid'
        
        return Response({'status': status_text}, status=status.HTTP_200_OK)


class LicenseDetailsView(generics.RetrieveAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer

