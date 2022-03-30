from django.urls import path
from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    LoginAPIView,
    PasswordChangeAPIView,
    CartAPIView,
    CartAddAPIView,
    CartRemoveAPIView,
    OrderedBooksAPIView,
    OrdersAPIView,
    OrderItemsAPIView,
    FakePaymentAPIView,
)

urlpatterns = [
    path('list/', UserListAPIView.as_view()),
    path('signup/', UserCreateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('<int:id>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('<int:id>/update/', UserUpdateAPIView.as_view()),
    path('<int:id>/change-password/', PasswordChangeAPIView.as_view()),

    path('<int:id>/cart/', CartAPIView.as_view(), name='cart'),
    path('<int:id>/cart/add/<slug:book_slug>/', CartAddAPIView.as_view(), ),
    path('<int:id>/cart/remove/<slug:book_slug>/', CartRemoveAPIView.as_view(), name='cart_remove'),
    path('<int:id>/cart/payment/', FakePaymentAPIView.as_view(), name='fake_payment'),
    
    path('<int:id>/books/', OrderedBooksAPIView.as_view(), name='user_books'),
    path('<int:id>/orders/', OrdersAPIView.as_view(), name='orders'),
    path('<int:id>/orders/<str:order_id>/', OrderItemsAPIView.as_view(), name='order_items'),

]


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