from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
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



class KnoxSocialLoginView(SocialLoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()
        
        if getattr(self, '_errors', None) is not None:
            return Response(self._errors, status=400)
        
        serializer = serializer_class(instance=self.token, context=self.get_serializer_context())
        
        # Create Knox token
        knox_token = AuthToken.objects.create(self.user)
        
        data = {
            'user': self.user,
            'token': knox_token[1]  # The token string
        }
        
        return Response(data)

class FacebookLogin(KnoxSocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'YOUR_FACEBOOK_CALLBACK_URL'

class GoogleLogin(KnoxSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'YOUR_GOOGLE_CALLBACK_URL'