from django.contrib import admin
from .models import Book, Author, Genre


@admin.register(Book)
class EbookAdmin(admin.ModelAdmin):
    exclude = ['slug',]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    exclude = ['slug',]

@admin.register(Genre)
class TagAdmin(admin.ModelAdmin):
    exclude = ['slug',]