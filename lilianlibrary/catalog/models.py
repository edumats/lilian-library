from django.db import models
from django.urls import reverse
import uuid

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    # May have to change to M2M
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, help_text='ISBN')
    genre = models.ManyToManyField('Genre', help_text='Genre(s) of the book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

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
