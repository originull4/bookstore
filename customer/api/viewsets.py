from crypt import methods
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, LoginSerializer, PasswordChangeSerializer
from rest_framework.permissions import BasePermission


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
        obj_related_actions = ['retrieve', 'update', 'destroy', 'partial_update', 'cart']
        if view.action in obj_related_actions:
            if not self.is_admin_or_owner(request, obj):
                return False
        if view.action == 'change_password':
            print('per')
            if not self.is_owner(request, obj):
                return False
        return True


class UserViewSet(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewSetPermission]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = Token.objects.get(user=user).key
        data = {
            'id': user.id,
            'username': user.username,
            'token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_name='change-password')
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = PasswordChangeSerializer(
            user, data=request.data, context={'request': request, 'user': user}
        )
        if serializer.is_valid():
            serializer.save()
            msg = {"detail": "password changed successfully"}
            return Response(msg, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')