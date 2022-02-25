from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import datetime
from django.shortcuts import redirect
from django.http import Http404  


def login_required(func):    
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/customer/login/?next={request.path}')
        else: return func(request, *args, **kwargs)
    return wrap

def logout_required(func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated: return func(request, *args, **kwargs)
        else: return redirect('home')
    return wrap

def generate_filename(filename, value):
    # get file extension
    ext = filename.split('.')[-1]
    # Returns the new name in lowercase and slugified
    return f'{slugify(str(value).lower())}.{ext}'

def avatar_upload(instance, filename):
    return f'avatars/{generate_filename(filename, instance.user.username)}'

def book_cover_upload(instance, filename):
    return f'book_covers/{generate_filename(filename, instance.title)}'

def pdf_upload(instance, filename):
    return f'pdfs/{generate_filename(filename, instance.title)}'

def validate_published_year(value):
    current_year = datetime.now().year
    if value and value not in range(1800, current_year):
        raise ValidationError(f'Invalid Year! Year must be between {current_year} and 1800.')