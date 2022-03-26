from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from core.utils import book_cover_upload, pdf_upload, validate_published_year


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='full name', unique=True)
    description = models.TextField(verbose_name='about author', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.name = str(self.name).lower()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(verbose_name='description', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.title = str(self.title).lower()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='about book', blank=True, null=True, max_length=2000)
    pages = models.PositiveIntegerField(default=10)
    language = models.CharField(max_length=100, blank=True, null=True, default='English')
    published_year = models.PositiveSmallIntegerField(blank=True, null=True, validators=[validate_published_year])
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cover = models.ImageField(upload_to=book_cover_upload, default='ebook_pictures/default.png')
    slug = models.SlugField(unique=True)
    pdf = models.FileField(upload_to=pdf_upload, validators=[FileExtensionValidator(['pdf'])])
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.title = str(self.title).lower()
        self.description = str(self.description).lower()
        self.language = str(self.language).lower()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title} by {self.author.name}'
