from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import User
from .serializers import (
    UserSignupSerializer, UserLoginSerializer, ProfileUpdateSerializer, 
    SearchSerializer, UserDeactivationSerializer, UserListSerializer, UserSerializer
)
from .custom_permission import IsHeadLibrarian, IsLibrarian, IsPatron


# Signup View
class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "Ready for signing up new users"}, status=status.HTTP_202_ACCEPTED)

# Login View
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print(f"Reqest.data: {request.data}")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # The user instance from validate()
            tokens = serializer.get_tokens(user)  # Get JWT tokens
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Allow the user to update their own profile, or allow head librarians and librarians to update any profile
        if user != request.user and not (request.user.is_superuser or request.user.role in ['head_librarian', 'librarian']):
            return Response({'detail': 'Not authorized to update this user'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Search Users View
class SearchUsersView(APIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian]

    def get(self, request):
        search_query = request.GET.get('q', '')
        users = User.objects.filter(email__icontains=search_query) | User.objects.filter(name__icontains=search_query)
        serializer = SearchSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Deactivate Users View
class DeactivateUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.role != 'head_librarian':
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()

        serializer = UserDeactivationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# User List View
class UserListView(APIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian]

    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            serializer = UserListSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = User.objects.all()
            serializer = UserListSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# User Search View
class UserSearchView(APIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian]
    User = get_user_model()

    def get(self, request):
        query = request.query_params.get('q', None)
        if query:
            users = User.objects.filter(
                Q(email__icontains=query) | Q(name__icontains=query)
            )
            user_data = [{"id": user.id, "email": user.email, "name": user.name, "role": user.role} for user in users]
            return Response(user_data, status=status.HTTP_200_OK)
        return Response({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            UntypedToken(token)
            return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)