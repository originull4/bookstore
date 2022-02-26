from django.urls import path
from .views import(
    books_view,
    book_detail_view,
    authors_view,
    genres_view,
)

app_name = 'book'
urlpatterns = [
    path('list/', books_view, name='books'),
    path('detail/<slug:book_slug>/', book_detail_view, name='book_detail'),
    path('authors/', authors_view, name='authors'),
    path('genres/', genres_view, name='genres'),
    path('genres/<slug:genre_slug>/', books_view, name='genre_books'),
    path('authors/<slug:author_slug>/', books_view, name='author_books'),
]
