from django.db import models
from django.urls import reverse
import uuid

class Author(models.Model):
    name = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField('Author', related_name='books')
    isbn = models.CharField('ISBN', max_length=13, help_text='ISBN')
    genre = models.ManyToManyField('Genre', help_text='Genre(s) of the book', blank=True, related_name='books')
    description = models.TextField(max_length=1000, blank=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, blank=True)
    date_added_to_library = models.DateField(auto_now_add=True)
    google_id = models.CharField(max_length=15, blank=True)
    number_pages = models.IntegerField(blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    thumbnail = models.URLField(blank=True)

    MEDIA_CHOICES = [
        ('B', 'Book'),
        ('E', 'E-Book'),
        ('A', 'Audiobook'),
    ]
    media_type = models.CharField(max_length=1, choices=MEDIA_CHOICES, default="B")

    def info_link(self):
        return f"https://books.google.com.br/books?id={google_id}=isbn:{isbn}"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Book genre')

    def __str__(self):
        return self.name



class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Library Unique ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('o', 'On Loan'),
        ('r', 'Reserved'),
        ('l', 'Lost'),
        ('m', 'Maintenance')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book Status'
    )

    def __str__(self):
        return f'ID: {self.id} - Title: {self.book.title}'


class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the book language')

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the book\'s publisher')

    def __str__(self):
        return self.name
