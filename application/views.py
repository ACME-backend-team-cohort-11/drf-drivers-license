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
    """
        Create a new driver's license application.
    """
    permission_classes = [permissions.IsAuthenticated]
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
        """
        Create a new driver's license application.

        Parameters:
        - is_motor_cycle (boolean): Whether the application is for a motorcycle license
        - is_motor_vehicle (boolean): Whether the application is for a motor vehicle license
        - certificate_number (integer): The certificate number
        - nationalId (integer): The National ID number of the applicant
        - application_type (string): The type of application (should be "New")
        - license_id (string): The license ID (should be empty for new applications)
        - status (string): The status of the application (e.g., "Pending")
        - local_government_area (string): The local government area
        - state (string): The state
        - center_locations (string): The center locations
        - email (string): The applicant's email address
        - phoneNumber (string): The applicant's phone number
        - reissue_reason (string): The reason for reissue (should be empty for new applications)
        - reissue_police_report (file): Police report for reissue (should be null for new applications)
        - previous_license_id (string): The previous license ID (should be empty for new applications)
        - renewal_applied_at (datetime): When the renewal was applied (should be null for new applications)
        - renewal_approved_at (datetime): When the renewal was approved (should be null for new applications)
        - reissue_applied_at (datetime): When the reissue was applied (should be null for new applications)
        - reissue_approved_at (datetime): When the reissue was approved (should be null for new applications)

        Returns:
        - 201 Created: Application created successfully
            {
                "application_id": "string (UUID)",
                "nationalId": integer,
                "is_motor_cycle": boolean,
                "is_motor_vehicle": boolean,
                "certificate_number": integer,
                "applied_at": "datetime",
                "application_type": "string",
                "status": "string",
                "local_government_area": "string",
                "state": "string",
                "center_locations": "string",
                "email": "string",
                "phoneNumber": "string",
                "previous_license_id": "string",
                "renewal_applied_at": "datetime or null",
                "renewal_approved_at": "datetime or null",
                "reissue_applied_at": "datetime or null",
                "reissue_approved_at": "datetime or null",
                "reissue_reason": "string",
                "reissue_police_report": "file or null",
                "license": "object or null"
            }
        - 400 Bad Request: Invalid data provided
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RenewDriversLicenseApplicationView(generics.CreateAPIView):
    """
    Create a renewal application for an existing driver's license.
    """
    permission_classes = [permissions.IsAuthenticated] 
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a renewal application for an existing driver's license.

        Parameters:
        - is_motor_cycle (boolean): Whether the application is for a motorcycle license
        - is_motor_vehicle (boolean): Whether the application is for a motor vehicle license
        - certificate_number (integer): The certificate number
        - nationalId (integer): The National ID number of the applicant
        - application_type (string): The type of application (should be "Renewal")
        - license_id (string): The ID of the license to renew
        - status (string): The status of the application (e.g., "Pending")
        - local_government_area (string): The local government area
        - state (string): The state
        - center_locations (string): The center locations
        - email (string): The applicant's email address
        - phoneNumber (string): The applicant's phone number
        - reissue_reason (string): The reason for reissue (should be empty for renewals)
        - reissue_police_report (file): Police report for reissue (should be null for renewals)
        - previous_license_id (string): The previous license ID (should be empty for renewals)
        - renewal_applied_at (datetime): When the renewal was applied (should be null)
        - renewal_approved_at (datetime): When the renewal was approved (should be null)
        - reissue_applied_at (datetime): When the reissue was applied (should be null)
        - reissue_approved_at (datetime): When the reissue was approved (should be null)

        Returns:
        - 201 Created: Renewal application created successfully
            {
                "message": "Renewal application submitted successfully.",
                "application_id": "string (UUID)"
            }
        - 400 Bad Request: Invalid data or existing renewal application
        - 404 Not Found: License not found
        """
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
    """
    Create a reissue application for an existing driver's license.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = DriversLicenseApplication.objects.all()
    serializer_class = DriversLicenseApplicationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        """
        Create a reissue application for an existing driver's license.

        This is a multipart form where the police report is uploaded as a file.

        Parameters:
        - is_motor_cycle (boolean): Whether the application is for a motorcycle license
        - is_motor_vehicle (boolean): Whether the application is for a motor vehicle license
        - certificate_number (integer): The certificate number
        - nationalId (integer): The National ID number of the applicant
        - application_type (string): The type of application (should be "Reissue")
        - license_id (string): The ID of the license to reissue
        - status (string): The status of the application (e.g., "Pending")
        - local_government_area (string): The local government area
        - state (string): The state
        - center_locations (string): The center locations
        - email (string): The applicant's email address
        - phoneNumber (string): The applicant's phone number
        - reissue_reason (string): The reason for reissue
        - reissue_police_report (file): Police report for reissue
        - previous_license_id (string): The previous license ID
        - renewal_applied_at (datetime): When the renewal was applied (should be null for reissues)
        - renewal_approved_at (datetime): When the renewal was approved (should be null for reissues)
        - reissue_applied_at (datetime): When the reissue was applied (should be null)
        - reissue_approved_at (datetime): When the reissue was approved (should be null)

        Returns:
        - 201 Created: Reissue application created successfully
            {
                "message": "Reissue application submitted successfully.",
                "application_id": "string (UUID)"
            }
        - 400 Bad Request: Invalid data or existing renewal application
        - 404 Not Found: License not found
        """
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
