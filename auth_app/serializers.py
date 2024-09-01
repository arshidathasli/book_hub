from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Serializer for user signup
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('role', 'email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'patron')  # Default role to 'patron'
        )
        return user

# Serializer for user login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate user
        user = authenticate(email=email, password=password)
        
        if user and user.is_active:
            return user
        else:
            raise serializers.ValidationError("Invalid credentials or inactive account.")
    
    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token['role'] = user.role

        return {
            'refresh': str(refresh),
            'access': str(access_token),
        }
    

# Serializer for listing all users
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
                                 
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'is_active']

from rest_framework import serializers
from django.contrib.auth import get_user_model

class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'is_active', 'role']  # Include all fields you want to update

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.role = validated_data.get('role', instance.role)

        if 'password' in validated_data:
            # Handle password update
            password = validated_data['password']
            if password:
                instance.set_password(password)

        if 'is_active' in validated_data:
            # Handle is_active status update
            instance.is_active = validated_data['is_active']

        instance.save()
        return instance


# Serializer for searching users
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'role')  

# Serializer for user deactivation
class UserDeactivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'is_active']           

# Serializer for listing users
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'role', 'is_active')
