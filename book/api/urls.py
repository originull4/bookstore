from django.urls import path

from .viewsets import AuthorViewSet, GenreViewSet, BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'books', BookViewSet, basename='book')

author_books = BookViewSet.as_view({'get': 'author_books'})
genre_books = BookViewSet.as_view({'get': 'genre_books'})

urlpatterns = [
    path('author/<slug>/books/', author_books, name='author-books'),
    path('genre/<slug>/books/', genre_books, name='genre-books'),
]

urlpatterns += router.urls
