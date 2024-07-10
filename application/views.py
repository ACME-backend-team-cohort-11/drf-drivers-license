# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import DriversLicenseApplication
from nationalId.models import NationalId
from license.models import License
from .serializers import DriversLicenseApplicationSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

class CreateDriversLicenseApplicationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer

    def perform_create(self, serializer):
        national_id_no = self.request.data.get('nationalId')
        try:
            national_id = NationalId.objects.get(pk=national_id_no)
        except NationalId.DoesNotExist:
            raise serializers.ValidationError("NationalId does not exist")
        
        serializer.save(nationalId=national_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RenewDriversLicenseApplicationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]  # Temporarily allow any user to access this view
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer

    def create(self, request, *args, **kwargs):
        license_id = self.kwargs.get('license_id')
        license = get_object_or_404(License, licenseId=license_id)

        # Get nationalId from request data
        national_id_no = request.data.get('nationalId')
        if not national_id_no:
            return Response({"error": "NationalId is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            national_id = NationalId.objects.get(pk=national_id_no)
        except NationalId.DoesNotExist:
            return Response({"error": "Invalid NationalId."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing renewal application
        existing_renewal = DriversLicenseApplication.objects.filter(
            nationalId=national_id,
            license=license,
            application_type='Renewal',
            status__in=['Renewal Pending', 'Renewal Processing']
        ).first()

        if existing_renewal:
            return Response({"error": "A renewal application for this license is already in progress."}, status=status.HTTP_400_BAD_REQUEST)

        
        # Additional check to see if a renewal application for the specific driver's license exists
        if DriversLicenseApplication.objects.filter(nationalId=national_id, license=license).exists():
            return Response({"error": "A renewal application for this license is already in progress."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the renewal application
        renewal_application, created = DriversLicenseApplication.objects.get_or_create(
        nationalId=national_id,
        license=license,
        defaults={
            'is_motor_cycle': request.data.get('is_motor_cycle'),
            'is_motor_vehicle': request.data.get('is_motor_vehicle'),
            'certificate_number': request.data.get('certificate_number'),
            'application_type': 'Renewal',  # Hardcoded as per your requirement
            'status': request.data.get('status'),
            'local_government_area': request.data.get('local_government_area'),
            'state': request.data.get('state'),
            'center_locations': request.data.get('center_locations'),
            'email': request.data.get('email'),
            'phoneNumber': request.data.get('phoneNumber'),
            'reissue_reason': request.data.get('reissue_reason'),
            'reissue_police_report': request.data.get('reissue_police_report'),
            'previous_license_id': request.data.get('previous_license_id'),
            'renewal_applied_at': timezone.now(),  # Assuming current time for now
            'renewal_approved_at': None,  
            'reissue_applied_at': None, 
            'reissue_approved_at': None,  
            }
        )

        return Response({
            "message": "Renewal application submitted successfully.",
            "application_id": renewal_application.application_id
        }, status=status.HTTP_201_CREATED)

class ReissueDriversLicenseApplicationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        license_id = request.data.get('license_id')
        if not license_id:
            return Response({"error": "License ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        license = get_object_or_404(License, licenseId=license_id)

        # Get nationalId from request data
        national_id_no = request.data.get('nationalId')
        if not national_id_no:
            return Response({"error": "NationalId is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            national_id = NationalId.objects.get(pk=national_id_no)
        except NationalId.DoesNotExist:
            return Response({"error": "Invalid NationalId."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing renewal application
        existing_renewal = DriversLicenseApplication.objects.filter(
            nationalId=national_id,
            license=license,
            application_type='Renewal',
            status__in=['Renewal Pending', 'Renewal Processing']
        ).exists()

        if existing_renewal:
            return Response({"error": "A renewal application for this license is already in progress."},status=status.HTTP_400_BAD_REQUEST)

        # Convert boolean fields from string to boolean
        is_motor_cycle = request.data.get('is_motor_cycle', '').lower() == 'true'
        is_motor_vehicle = request.data.get('is_motor_vehicle', '').lower() == 'true'

        # Extract reissue reason
        reissue_reason = request.data.get('reissue_reason')

        # Handle uploaded police report file
        reissue_police_report = request.FILES.get('reissue_police_report')

        # Create or update the reissue application
        reissue_application = DriversLicenseApplication.objects.create(
            nationalId=national_id,
            license=license,
            application_type='Reissue',  # Hardcoded as per your requirement
            status='Reissue Pending',  # Assuming initial status
            is_motor_cycle=is_motor_cycle,
            is_motor_vehicle=is_motor_vehicle,
            certificate_number=request.data.get('certificate_number'),
            local_government_area=request.data.get('local_government_area'),
            state=request.data.get('state'),
            center_locations=request.data.get('center_locations'),
            email=request.data.get('email'),
            phoneNumber=request.data.get('phoneNumber'),
            reissue_reason=reissue_reason,
            reissue_police_report=reissue_police_report,
            previous_license_id=request.data.get('previous_license_id'),
            reissue_applied_at=timezone.now(),  # Assuming current time for reissue
            reissue_approved_at=None,
        )

        return Response({
            "message": "Reissue application submitted successfully.",
            "application_id": reissue_application.application_id
        }, status=status.HTTP_201_CREATED)

class RetrieveDriversLicenseApplicationView(generics.RetrieveAPIView):
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer
