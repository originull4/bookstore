from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home, name='home'),
    path('', RedirectView.as_view(pattern_name='home')),

    path('customer/', include('customer.urls', namespace='customer')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
