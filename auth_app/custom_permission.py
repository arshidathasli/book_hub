from rest_framework.permissions import BasePermission

class IsHeadLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'head_librarian'

class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'librarian'

class IsPatron(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patron'
