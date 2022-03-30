from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm, UserUpdateForm, CustomerUpdateForm
from .models import Order, OrderItem
from book.models import Book
from core.utils import login_required, logout_required


@logout_required
def signup_view(request):
    template = 'customer/signup.html'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'your account has been created successfully and you are logged in.')
            return redirect('customer:profile')
        messages.error(request, 'signup failed!!! check your infromations and try again.')
    else: form = UserCreationForm
    return render(request, template, {'form': form})


@logout_required
def login_view(request):
    template = 'customer/login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                messages.success(request, 'you are logged in successfully.')
                if 'next' in request.POST: return redirect (request.POST.get('next'))
                return redirect('customer:profile')
            messages.error(request, 'username or password is incorrect.  please try again.')
    else: form = LoginForm
    return render(request, template, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    template = 'customer/profile.html'
    return render(request, template, {'user': request.user, 'customer': request.user.customer})


@login_required
def profile_update_view(request):
    template = 'customer/profile_update.html'
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=user)
        customer_form = CustomerUpdateForm(data=request.POST, files=request.FILES, instance=user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, 'profile has been updated successfully.')
            return redirect('customer:profile')
        messages.error(request, 'update failed!!!. please check your information and try again.')
    else:
        user_form = UserUpdateForm(instance=user)
        customer_form = CustomerUpdateForm(instance=user.customer)
    return render(request, template, {'user_form': user_form, 'customer_form': customer_form})


@login_required
def password_update_view(request):
    template = 'customer/password_update.html'
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'your password has been changed successfully.')
            return redirect('customer:profile')
        messages.error(request, 'password change failed!!!. please check your information and try again.')
    else: form = PasswordChangeForm(user=request.user)
    return render(request, template, {'form': form})


@login_required
def cart_add_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    OrderItem.objects.get_or_create(order=request.user.customer.cart, book=book)
    request.user.customer.update_cart_total_price()
    messages.success(request, f'{book} added to your cart.')
    return redirect('book:book_detail', book_slug=book.slug)
    

@login_required
def cart_remove_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    order_item = get_object_or_404(OrderItem, order=request.user.customer.cart, book=book)
    order_item.delete()
    request.user.customer.update_cart_total_price()
    messages.success(request, f'{book} removed from your cart.')
    sender = request.GET.get('sender')
    if sender == 'cart': return redirect('customer:cart')
    return redirect('book:book_detail', book_slug=book.slug)
    

@login_required
def cart_view(request):
    template = 'customer/cart.html'
    cart_items = [item.book for item in request.user.customer.cart.items.all()]
    return render(request, template, {'cart_items': cart_items})


@login_required
def checkout_view(request):
    template = 'customer/checkout.html'
    cart_items = [item.book for item in request.user.customer.cart.items.all()]
    if len(cart_items) == 0:
        messages.error(request, 'your cart is empty, first add some book in your cart')
        return redirect('book:book_list')
    return render(request, template, {'cart_items': cart_items})


@login_required
def fake_payment_view(request):
    customer = request.user.customer
    order = customer.cart
    
    if order.items.all().count() == 0:
        messages.error(request, "you haven't any pending order.")
        return redirect('customer:cart')

    order.amount = customer.cart_total_price
    order.complete = True
    order.dete_completed = datetime.now()
    order.save()

    messages.success(request, 'your payment was successfully processed.')

    return redirect('customer:receipt', order_id=order.order_id)


@login_required
def receipt_view(request, order_id):
    template = 'customer/receipt.html'
    order = get_object_or_404(Order, pk=order_id)
    return render(request, template, {'order': order})


@login_required
def user_books_view(request):
    template = 'customer/user_books.html'
    books = request.user.customer.ordered_books
    return render(request, template, {'books': books})


@login_required
def orders_view(request):
    template = 'customer/orders.html'
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, template, {'orders': orders})


@login_required
def order_items_view(request, order_id):
    template = 'customer/order_items.html'
    order = get_object_or_404(Order, pk=order_id)
    return render(request, template, {'order': order})