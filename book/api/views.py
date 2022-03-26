from functools import partial
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from book.models import Author, Genre, Book
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer


class IsAdminOrReadOnly(BasePermission):
    """
    permission to staff users to GET request
    only superuser users cat access to POST, PUT, DELETE requests
    """
    
    def has_permission(self, request, *args):
        if request.method in SAFE_METHODS: return True
        if request.user.is_superuser: return True
        return False


class AuthorAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, **kwargs):
        authors = Author.objects.all()
        if 'author_slug' in kwargs:
            authors = authors.filter(slug=kwargs['author_slug'])
        serializer = AuthorSerializer(authors, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        serializer = AuthorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        author = get_object_or_404(Author, slug=kwargs['author_slug'])
        serializer = AuthorSerializer(author, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        author = get_object_or_404(Author, slug=kwargs['author_slug'])
        author.delete()
        msg = {'detail': f'{author} was deleted.'}
        return Response(msg, status=status.HTTP_204_NO_CONTENT)


class GenreAPIView(APIView):

    def get(self, request, **kwargs):
        genres = Genre.objects.all()
        if 'genre_slug' in kwargs:
            genres = genres.filter(slug=kwargs['genre_slug'])
        serializer = GenreSerializer(Genre.objects.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookAPIView(APIView):

    def get(self, request, **kwargs):
        books = Book.objects.all()
        book_title = request.GET.get('book_title')
        if book_title: books = books.filter(title__icontains=book_title)
        if 'book_slug' in kwargs:  books = books.filter(slug=kwargs['book_slug'])
        if 'genre_slug' in kwargs:  books = books.filter(genres__slug=kwargs['genre_slug'])
        if 'author_slug' in kwargs: books = books.filter(author__slug=kwargs['author_slug'])
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



# from .views import (
#     AuthorAPIView,
#     GenreAPIView,
#     BookAPIView,
# )

# urlpatterns = [
#     path('authors/', AuthorAPIView.as_view(), name='authors-list'),
#     path('author/<slug:author_slug>/', AuthorAPIView.as_view(), name='author-detail'),
#     path('author/<slug:author_slug>/books/', BookAPIView.as_view(), name='author-books'),
#     path('author/create/', AuthorAPIView.as_view(), name='author-create'),
#     path('author/<slug:author_slug>/update/', AuthorAPIView.as_view(), name='author-update'),
#     path('genres/', GenreAPIView.as_view(), name='genres-list'),
#     path('genre/<slug:genre_slug>/', GenreAPIView.as_view(), name='genre-detail'),
#     path('', BookAPIView.as_view(), name='books-list'),
#     path('<slug:book_slug>/', BookAPIView.as_view(), name='book-detail'),
#     path('genre/<slug:genre_slug>/books/', BookAPIView.as_view(), name='genre-books'),
# ]