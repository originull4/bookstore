from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from book.models import Author, Genre, Book


class AuthorSerializer(ModelSerializer):
    author_detail_url = HyperlinkedIdentityField(
        view_name='author-detail',
        lookup_field='slug',
        read_only=True
    )
    author_books_url = HyperlinkedIdentityField(
        view_name='author-books',
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True},
        }


    
class GenreSerializer(ModelSerializer):
    genre_detail_url = HyperlinkedIdentityField(
        view_name='genre-detail',
        lookup_field='slug',
        read_only=True
    )
    genre_books_url = HyperlinkedIdentityField(
        view_name='genre-books',
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = Genre
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True},
        }


class BookSerializer(ModelSerializer):
    # author_name = CharField(source='author.name', read_only=True)
    # genres = StringRelatedField(many=True)
    # author = AuthorSerializer()
    # genres = GenreSerializer(many=True, read_only=True)
    book_detail_url = HyperlinkedIdentityField(
        view_name='book-detail',
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True},
        }