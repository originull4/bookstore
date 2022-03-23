from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, LoginSerializer, PasswordChangeSerializer


class UserCreateAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {'user': serializer.data, 'token': token}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(APIView):

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsAdminUser,]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
       
        if user == request.user or user.is_superuser:
            serializer = UserSerializer(user, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        msg = {'permission error': 'you do not have permission to perform this action.'}
        return Response(msg, status=status.HTTP_403_FORBIDDEN)


class UserUpdateAPIView(APIView):

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def put(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])

        if user == request.user or user.is_superuser:
            serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        msg = {'permission error': 'you do not have permission to perform this action.'}
        return Response(msg, status=status.HTTP_403_FORBIDDEN)


class LoginAPIView(APIView):

    def post(self, request):
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


class PasswordChangeAPIView(APIView):
    
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def put(self, request, **kwargs):

        user = get_object_or_404(User, pk=kwargs['id'])
        
        if request.user != user:
            msg = {"detail": "You do not have permission to perform this action."}
            return Response(msg, status = status.HTTP_403_FORBIDDEN)

        serializer = PasswordChangeSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            msg = {"detail": "password changed successfully"}
            return Response(msg, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)