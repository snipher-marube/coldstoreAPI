import requests
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.helpers import complete_social_login
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


class GoogleLogin(APIView):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'Authorization code not provided'}, status=400)

        try:
            # Get Google app credentials
            app = SocialApp.objects.get(provider='google')
            
            # Exchange code for tokens
            token_url = 'https://oauth2.googleapis.com/token'
            data = {
                'code': code,
                'client_id': app.client_id,
                'client_secret': app.secret,
                'redirect_uri': 'http://localhost:8000/api/v1/auth/google/',
                'grant_type': 'authorization_code'
            }
            
            token_response = requests.post(token_url, data=data)
            token_data = token_response.json()
            
            if 'access_token' not in token_data:
                return Response({'error': 'Failed to obtain access token'}, status=400)
            
            # Get user info from Google
            user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
            headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
            user_info = requests.get(user_info_url, headers=headers).json()
            
            # Get or create user
            User = get_user_model()
            email = user_info.get('email')
            
            if not email:
                return Response({'error': 'Email not provided by Google'}, status=400)
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create new user
                username = email.split('@')[0]
                user = User.objects.create(
                    email=email,
                    username=username,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', '')
                )
                user.set_unusable_password()
                user.save()
            
            # Create Knox token
            _, token = AuthToken.objects.create(user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'token': token
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=400)