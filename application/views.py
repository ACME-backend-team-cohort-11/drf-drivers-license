# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import DriversLicenseApplication
from .serializers import DriversLicenseApplicationSerializer
from django.utils import timezone

class CreateDriversLicenseApplicationView(generics.CreateAPIView):
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer

    def perform_create(self, serializer):
        # Assign current user to the application before saving
        serializer.save(user=self.request.user.id)  # Assuming request.user.id is the NationalId instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RenewDriversLicenseApplicationView(generics.UpdateAPIView):
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer

    def perform_update(self, serializer):
        # Update renewal-related fields
        serializer.save(status='Renewal Pending', renewal_applied_at=timezone.now())

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.update(request, *args, **kwargs)

class ReissueDriversLicenseApplicationView(generics.UpdateAPIView):
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer

    def perform_update(self, serializer):
        # Update reissue-related fields
        serializer.save(status='Reissue Pending', reissue_applied_at=timezone.now())

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.update(request, *args, **kwargs)

class ListDriversLicenseApplicationsView(generics.ListAPIView):
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer


class RetrieveDriversLicenseApplicationView(generics.RetrieveAPIView):
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer
