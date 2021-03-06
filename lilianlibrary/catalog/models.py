from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

class Author(models.Model):
    name = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    # Only title is required
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField('Author', related_name='books', blank=True)
    # If data is inserted, it must be unique.
    # It can also be left as blank without unique contraint violation
    isbn_10 = models.CharField('ISBN 10', max_length=10, help_text='ISBN 10', unique=True, blank=True, null=True)
    isbn_13 = models.CharField('ISBN 13', max_length=13, help_text='ISBN 13', unique=True, blank=True, null=True)
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
    tags = models.ManyToManyField('Tag', related_name='tags', blank=True)

    def info_link(self):
        return f"https://books.google.com.br/books?id={google_id}=isbn:{isbn}"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    def display_author(self):
        return ', '.join(author.name for author in self.authors.all()[:3])

    display_genre.short_description = 'Genre'

    display_author.short_description = 'Authors'

    class Meta:
        ordering = ['title']


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Book genre')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Library Unique ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(max_length=1000, blank=True)

    MEDIA_CHOICES = [
        ('B', 'Book'),
        ('E', 'E-Book'),
        ('A', 'Audiobook'),
    ]
    media_type = models.CharField(max_length=1, choices=MEDIA_CHOICES, default="B")

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
        return f'ID: {self.book} - Status: {self.status}'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the book language')

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the book\'s publisher')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('publisher-detail', args=[str(self.id)])

class Quote(models.Model):
    quote = models.TextField(max_length=1000, help_text='Enter your favourite quote')
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.quote

class Tag(models.Model):
    name = models.TextField(max_length=100, help_text='Enter your tag')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag-detail', args=[str(self.id)])
