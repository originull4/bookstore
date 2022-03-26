from .viewsets import UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls


# 'users/' [name='user-list'] GET -> return users list
# 'users/' [name='user-list'] POST -> create new staff user
# 'users/<int:pk>/' [name='user-detail'] GET -> return user detail
# 'users/<int:pk>/' [name='user-detail'] PUT -> update user detail
# 'users/<int:pk>/' [name='user-detail'] DELETE -> delete user
# 'users/login/' [name='user-login'] POST -> return user token key
# 'users/<int:pk>/change_password/' [name='user-change-password'] POST -> change password