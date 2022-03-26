from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

class UserViewSetPermission(BasePermission):

    def get_token(self, request):
        """
        Returns `Token` if token key is correct, otherwise returns `False`.
        """
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth : return False
        if not isinstance(auth, str): return False
        auth = auth.split()
        if len(auth) != 2: return False
        if auth[0].lower() != 'token': return False
        return auth[1]

    def is_admin(self, request):
        token = self.get_token(request)
        user = get_object_or_404(Token, key=token).user
        if user.is_superuser:
            return True
        else: return False

    def is_admin_or_owner(self, request, obj):
        token = self.get_token(request)
        user = get_object_or_404(Token, key=token).user
        if user.is_superuser: return True
        if obj.auth_token.key == token:
            return True
        return False

    def is_owner(self, request, obj):
        token = self.get_token(request)
        user = get_object_or_404(Token, key=token).user
        if obj == user: return True
        return False


    def has_permission(self, request, view, *args, **kwargs):
        if view.action == 'list':   
            if not self.is_admin(request):
                return False        
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'destroy', 'partial_update']:
            if not self.is_admin_or_owner(request, obj):
                return False
        if view.action == 'change_password':
            print('per')
            if not self.is_owner(request, obj):
                return False
        return True
