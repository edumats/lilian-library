import os, requests, json
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from .forms import isbnForm

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    horror_books = Book.objects.filter(genre__name__iexact='horror').count()

    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'horror_books': horror_books,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

def add(request):
    if request.method == 'POST':
        pass

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

        print(f"Items: {data['totalItems']}")
        print(f"Type: {type(data['totalItems'])}")

        # If no books were found, API will return object with totalItems = 0
        if data['totalItems'] == 0:
            # Return success: False to display an error page
            return render(request, 'confirm_book.html', {'success': False})

        # Defining variables for cleaner code
        book_data = data['items'][0]['volumeInfo']
        book_id = data['items'][0]['volumeInfo']['industryIdentifiers'][0]

        context = {
            'success': True,
            'title': book_data.get('title', 'No title'),
            'authors': book_data.get('authors', 'No authors'),
            'publisher': book_data.get('publisher', 'No publisher'),
            'pages': book_data.get('pageCount', 'No page count'),
            'description': book_data.get('description', 'No description'),
            'isbn': book_id.get('identifier', 'No ISBN'),
            'thumbnail': book_data.get('imageLinks', 'No image available').get('thumbnail', 'No thumbnail'),
            'language': book_data.get('language', 'No language'),
            'published_date': book_data.get('publishedDate', 'No published date'),
            'print_type': book_data.get('printType', 'No print type'),
            'categories': book_data.get('categories', 'No categories')
        }

        return render(request, 'confirm_book.html', context=context)


class BookListView(generic.ListView):
    model = Book

class BookDetailsView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailsView(generic.DetailView):
    model = Author
