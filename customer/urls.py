from django.urls import path
from .views import(
    signup_view,
    login_view,
    logout_view,
    profile_view,
    profile_update_view,
    password_update_view,
    cart_add_view,
    cart_remove_view,
    cart_view,
    checkout_view,
    fake_payment_view,
    receipt_view,
    user_books_view,
    orders_view,
    order_items_view,
)


app_name = 'customer'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
    path('password/update/', password_update_view, name='password_update'),

    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:book_id>/', cart_add_view, name='cart_add'),
    path('cart/remove/<int:book_id>/', cart_remove_view, name='cart_remove'),

    path('cart/checkout/', checkout_view, name='checkout'),
    path('cart/payment/', fake_payment_view, name='fake_payment'),

    path('orders/receipt/<str:order_id>/', receipt_view, name='receipt'),
    path('books/', user_books_view, name='user_books'),
    path('orders/', orders_view, name='orders'),
    path('orders/items/<str:order_id>/', order_items_view, name='order_items'),

]