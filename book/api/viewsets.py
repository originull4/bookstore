from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters


from .serializers import AuthorSerializer, BookSerializer, GenreSerializer
from book.models import Author, Book, Genre


class IsAdminOrReadOnly(BasePermission):
    """
    permission to staff users to GET request
    only superuser users cat access to POST, PUT, DELETE requests
    """
    
    def has_permission(self, request, *args):
        if request.method in SAFE_METHODS: return True
        if request.user.is_superuser: return True
        return False

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]


    @action(detail=False)
    def author_books(self, request, slug):
        books = self.get_queryset().filter(author__slug=slug)
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=False)
    def genre_books(self, request, slug):
        books = self.get_queryset().filter(genres__slug=slug)
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)
