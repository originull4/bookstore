from django.urls import path
from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserCreateAPIView,
    UserUpdateAPIView,
    LoginAPIView,
    PasswordChangeAPIView,
    
)

urlpatterns = [
    path('create/', UserCreateAPIView.as_view()),
    path('list/', UserListAPIView.as_view()),
    path('detail/<int:id>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('update/<int:id>/', UserUpdateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('password/change/<int:id>/', PasswordChangeAPIView.as_view())
]