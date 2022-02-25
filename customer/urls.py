from django.urls import path
from .views import(
    signup_view,
    login_view,
    logout_view,
    profile_view,
    profile_update_view,
    password_update_view,
)


app_name = 'customer'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
    path('password/update/', password_update_view, name='password_update'),
]