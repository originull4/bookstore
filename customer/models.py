from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from uuid import uuid4
from core.utils import avatar_upload
from book.models import Book
from rest_framework.authtoken.models import Token

class Customer(models.Model):
    GENDER_CHOICES = (('Male', 'Male'),('Female', 'Female'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, blank=True, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to=avatar_upload, default='avatars/default.png')

    @property
    def ordered_books(self):
        books = []
        completed_orders = [order for order in self.orders.all() if order.complete]
        for order in completed_orders:
            for item in order.items.all(): books.append(item.book)
        return books

    @property
    def cart(self):
        order, order_created = Order.objects.get_or_create(customer=self, complete=False)
        return order
        
    @property
    def cart_total_price(self):
        return sum([item.book.price for item in self.cart.items.all()])

    def update_cart_total_price(self):
        cart = self.cart
        cart.amount = self.cart_total_price
        cart.save()
    

    def book_status(self, book):
        if book in self.ordered_books: return 3
        elif book in [item.book for item in self.cart.items.all()]: return 2
        else: return 1

    def __str__(self) -> str:
        return self.user.username


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid4, editable=False) # will be used for refrence code
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    date_added = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    complete = models.BooleanField(default=False)
    dete_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.customer.user.username} ({str(self.order_id)})'

    class Meta:
        ordering = ['-date_added']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.order.customer.user.username}, {self.book.title}'


# create customer object for user when new user created
# generate a token for the new user
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        Token.objects.create(user=instance)
    instance.customer.save()



