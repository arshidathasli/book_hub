from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from auth_app.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('role', 'email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'patron')  # Use default 'patron' if role is not provided
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate user using Django's built-in authentication
        user = authenticate(email=email, password=password)
        
        if user and user.is_active:
            # If authentication is successful, return user instance
            return user
        else:
            raise serializers.ValidationError("Invalid credentials or inactive account.")
    
    def get_tokens(self, user):
        # Generate JWT tokens for the user using SimpleJWT
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password']  # Add any other fields you'd like to make updatable

    # def validate_password(self, value):
    #     # If a password is provided, ensure it's secure
    #     if value and len(value) < 8:
    #         raise serializers.ValidationError("Password must be at least 8 characters long.")
    #     return value

    def update(self, instance, validated_data):
        # Update user details
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.role = validated_data.get('role', instance.role)
        
        # If password is provided, set a new password
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'role')  

class UserDeactivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'is_active']           