from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Genre


def books_view(request, **kwargs):
    template = 'book/books.html'
    books = Book.objects.all()
    book_title = request.GET.get('book_title')
    if book_title: books = books.filter(title__icontains=book_title)
    if 'genre_slug' in kwargs:  books = books.filter(genres__slug=kwargs['genre_slug'])
    if 'author_slug' in kwargs: books = books.filter(author__slug=kwargs['author_slug'])
    return render(request, template, {'books': books})

def book_detail_view(request, book_slug):
    template = 'book/book_detail.html'
    book = get_object_or_404(Book, slug=book_slug)
    if not request.user.is_authenticated: status = 0
    else: status = request.user.customer.book_status(book)
    return render(request, template, {'book': book, 'status': status})

def authors_view(request):
    template = 'book/authors.html'
    author_name = request.GET.get('author_name')
    if author_name: authors = Author.objects.filter(name__icontains=author_name)
    else: authors = Author.objects.all()
    return render(request, template, {'authors': authors})

def genres_view(request):
    template = 'book/genres.html'
    genre_title = request.GET.get('genre_title')
    if genre_title: genres = Genre.objects.filter(title__icontains=genre_title)
    else: genres = Genre.objects.all()
    return render(request, template, {'genres': genres})