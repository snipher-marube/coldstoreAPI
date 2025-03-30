from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class RegisterAPI(generics.CreateAPIView):
    """
    User registration endpoint.
    Creates a new user and returns an authentication token.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token and prepare response data
        _, token = AuthToken.objects.create(user)
        response_data = {
            'user': serializer.data,
            'token': token
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginAPI(generics.GenericAPIView):
    """
    User login endpoint.
    Authenticates user and returns an authentication token.
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Create token and prepare response data
        _, token = AuthToken.objects.create(user)
        response_data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'user_type': user.user_type,
            },
            'token': token
        }
        
        return Response(response_data, status=status.HTTP_200_OK)