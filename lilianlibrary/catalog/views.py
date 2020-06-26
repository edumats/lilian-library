import os, requests, json
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre, Language, Publisher
from .forms import isbnForm

def index(request):

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

def add(request):
    if request.method == 'POST':
        # Get previously saved book data in sessions
        book_data = request.session['scanned_book']
        # Get ISBN 10
        isbn_10 = book_data['isbn_10']

        # Check if book already exists in database
        if Book.objects.filter(isbn_10=isbn_10).exists():
            return render(request, 'confirm_book.html', {'success': False, 'message': 'This book already exists in the library'})

        # Finds or creates Publisher instance
        publisher, created = Publisher.objects.get_or_create(name=book_data['publisher'])

        # Finds or creates Language instance
        language, created = Language.objects.get_or_create(name=book_data['language'])

        # Creates Book instance
        book = Book.objects.create(
            title=book_data['title'],
            number_pages=book_data['pages'],
            description=book_data['description'],
            isbn_10=isbn_10,
            isbn_13=book_data['isbn_13'],
            thumbnail=book_data['thumbnail'],
            ratings_count=book_data['ratings_count'],
            average_rating=book_data['average_rating'],
            publisher=publisher,
            language=language,
            google_id=book_data['google_id'],

        )

        # Iterate over authors list
        for author in book_data['authors']:
            writer, created = Author.objects.get_or_create(name=author)
            book.authors.add(writer)

        # Iterate over book genres list
        for category in book_data['categories']:
            genre, created = Genre.objects.get_or_create(name=category)
            book.genre.add(genre)

        form = isbnForm()

        context = {
            'success': True,
            'form': isbnForm,
            'message': 'Book was successfuly added'
        }
        return render(request, 'add_book.html', context)

    else:
        form = isbnForm()
        return render(request, 'add_book.html', {'form': isbnForm})


def check(request):
    if request.method == 'GET':
        # Get ISBN from GET request
        isbn = request.GET.get('isbn')

        # Get Google Books API key from env variable
        key = os.environ.get('GOOGLE_BOOKS_API_KEY')

        # Make a GET call to Google Books API
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={key}')
        data = response.json()

        # If no books were found, API will return object with totalItems = 0
        if data['totalItems'] == 0:
            # Return success: False to display an error page
            return render(request, 'confirm_book.html', {'success': False, 'message': 'No book with the provided ISBN was found'})

        # Defining variables for cleaner code
        book_data = data['items'][0]['volumeInfo']
        isbn_10 = data['items'][0]['volumeInfo']['industryIdentifiers'][0]
        isbn_13 = data['items'][0]['volumeInfo']['industryIdentifiers'][1]
        isbn_container = data['items'][0]['volumeInfo']['industryIdentifiers']



        context = {
            'success': True,
            'title': book_data.get('title', 'No title'),
            # Gets a list
            'authors': book_data.get('authors', 'No authors'),
            'publisher': book_data.get('publisher', 'No publisher'),
            'pages': book_data.get('pageCount', 'No page count'),
            'description': book_data.get('description', 'No description'),
            'isbn_10': isbn_10.get('identifier', 'No ISBN 10'),
            'isbn_13': isbn_13.get('identifier', 'No ISBN 13'),
            # Empty string if no thumbnail is available
            'thumbnail': book_data.get('imageLinks', '').get('thumbnail', ''),
            'language': book_data.get('language', 'No language'),
            'published_date': book_data.get('publishedDate', 'No published date'),
            'print_type': book_data.get('printType', 'No print type'),
            # Gets a list
            'categories': book_data.get('categories', 'No categories'),
            'average_rating': book_data.get('averageRating', 0),
            'ratings_count': book_data.get('ratingsCount', 0),
            'google_id': data['items'][0].get('id', ''),
        }

        # Store book data in sessions for later insertion in database
        # User still needs to confirm if this data belongs to the scanned book
        request.session['scanned_book'] = context;

        return render(request, 'confirm_book.html', context=context)


class BookListView(generic.ListView):
    model = Book

class BookDetailsView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailsView(generic.DetailView):
    model = Author
