from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserSignupSerializer, UserLoginSerializer, ProfileUpdateSerializer, SearchSerializer, UserDeactivationSerializer

# urlpatterns = [
#     path('signup/', admin.site.urls),
#     path('login/', admin.site.urls),
#     path('update_profile/', admin.site.urls),
#     path('search_users/', admin.site.urls),
#     path('deactivate_users/', admin.site.urls),
# ]


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "Ready for signing up new users"}, status=status.HTTP_202_ACCEPTED)

{
"email": "patron2@g.com",
"password": "asdf"
}

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # The user instance from validate()
            tokens = serializer.get_tokens(user)  # Get JWT tokens
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this

    def get(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Search_Users(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if the user has permission to search
        if request.user.role not in ['librarian', 'head_librarian']:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Get search parameters from query parameters
        search_query = request.GET.get('q', '')

        # Filter users based on the search query
        User = get_user_model()
        users = User.objects.filter(email__icontains=search_query) | User.objects.filter(name__icontains=search_query)

        # Serialize the user data
        serializer = SearchSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeactivateUsers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Check if the user is a head librarian
        if request.user.role != 'head_librarian':
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Get the user to be deactivated
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Deactivate the user
        user.is_active = False
        user.save()

        # Serialize and return the response
        serializer = UserDeactivationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)