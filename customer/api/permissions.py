from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj