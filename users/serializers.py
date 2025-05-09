from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import serializers, validators

from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), 'A user with that email already exists'
                    )
                ]
            }
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value  # Return raw password, hash in create()

    def create(self, validated_data):
        # Hash password before creating user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)  # Let ModelSerializer handle creation

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email').lower()  # Normalize email to lowercase
        password = attrs.get('password')

        if email and password:
            # Try both email and username authentication
            user = authenticate(
                request=self.context.get('request'),
                username=email,  # Try email as username first
                password=password
            )
            
            # If that fails, try getting by email directly
            if not user:
                try:
                    user = User.objects.get(email__iexact=email)
                    if not user.check_password(password):
                        user = None
                except User.DoesNotExist:
                    user = None

            if not user:
                raise serializers.ValidationError({
                    'error': 'Invalid credentials',
                    'detail': 'The provided email or password was incorrect'
                })
        else:
            raise serializers.ValidationError({
                'error': 'Missing credentials',
                'detail': 'Both email and password are required'
            })
        
        attrs['user'] = user
        return attrs