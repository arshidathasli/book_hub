from django.contrib import admin
from django.urls import path, include
from .views import SignupView, LoginView, UpdateProfileView, Search_Users, DeactivateUsers

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('search_users/', Search_Users.as_view(), name='search_users'),
    path('deactivate_users/<int:user_id>/', DeactivateUsers.as_view(), name='deactivate_users'),
]
