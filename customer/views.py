from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm, UserUpdateForm, CustomerUpdateForm
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


