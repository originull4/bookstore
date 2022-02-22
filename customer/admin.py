from django.contrib import admin
from .models import Customer, Order, OrderItem

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
