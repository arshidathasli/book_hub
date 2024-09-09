from django.contrib import admin
from django.urls import path, include
from .views import (SignupView, LoginView, UpdateProfileView, SearchUsersView, DeactivateUsersView, UserListView, UserSearchView,
    VerifyTokenView, UpdateProfileSelfView,
    )

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('update_profile_self/', UpdateProfileSelfView.as_view(), name='update_profile_self'),
    path('update_profile/<int:user_id>/', UpdateProfileView.as_view(), name='update_profile'),
    path('search_users/', SearchUsersView.as_view(), name='search_users'),
    path('deactivate_users/<int:user_id>/', DeactivateUsersView.as_view(), name='deactivate_users'),
    path('userlist/', UserListView.as_view(), name='userlist'),
    path('userlist/<int:user_id>/', UserListView.as_view(), name='user_detail'),
    path('user_search/', UserSearchView.as_view(), name='user_search'),
    path('verify/', VerifyTokenView.as_view(), name='verify'),
]
