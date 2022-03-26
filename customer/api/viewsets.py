from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, LoginSerializer, PasswordChangeSerializer
from .permissions import UserViewSetPermission



class UserViewSet(ModelViewSet):
    """
    'users/' [name='user-list'] GET -> return users list (required admin user with token authentication)
    'users/<int:pk>/' [name='user-detail'] GET -> return user detail (is admin or is owner required with token authentication)
    'users/<int:pk>/' [name='user-detail'] PUT -> update user (is admin or is owner required with token authentication)
    'users/<int:pk>/' [name='user-detail'] PATCH -> partial update (is admin or is owner required with token authentication)
    'users/<int:pk>/' [name='user-detail'] DELETE -> delete user (is admin or is owner required with token authentication)
    'users/' [name='user-list'] POST -> create new staff user
    'users/login/' [name='user-login'] POST -> return user token key
    'users/<int:pk>/change_password/' [name='user-change-password'] POST -> change password (is owner required with token authentication)
    """
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


