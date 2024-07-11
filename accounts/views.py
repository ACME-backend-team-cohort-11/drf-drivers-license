"""Account views."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model, authenticate

class RegisterView(APIView):
    """
    API view for user registration.

    post:
    Register a new user and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user.

        Parameters:
        - email (string): User's email address
        - password (string): User's password
        - other fields as required by CustomUserSerializer

        Returns:
        - 201 Created: User registered successfully
            {
                'refresh': 'refresh_token',
                'access': 'access_token'
            }
        - 400 Bad Request: Invalid data
            {
                'field_name': ['error_message']
            }
        """
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class LoginView(APIView):
    """
    API view for user login.

    post:
    Authenticate a user and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate a user.

        Parameters:
        - email (string): User's email address
        - password (string): User's password

        Returns:
        - 200 OK: User authenticated successfully
            {
                'refresh': 'refresh_token',
                'access': 'access_token'
            }
        - 400 Bad Request: Missing email or password
        - 401 Unauthorized: Invalid credentials
        """
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Please provide both email and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        email = email.lower()
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """
    API view for user logout.

    post:
    Blacklist the user's refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout a user by blacklisting their refresh token.

        Parameters:
        - refresh_token (string): User's refresh token

        Returns:
        - 205 Reset Content: Successfully logged out
        - 400 Bad Request: Invalid token or other error
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
