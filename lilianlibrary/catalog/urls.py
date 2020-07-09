from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailsView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailsView.as_view(), name='author-detail'),
    path('check/', views.check, name='check'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('add/', views.add, name='add'),
    path('tag/<int:pk>', views.TagDetailsView.as_view(), name='tag-detail'),
    path('genre/<int:pk>', views.GenreDetailsView.as_view(), name='genre-detail'),
    path('publisher/<int:pk>', views.PublisherDetailsView.as_view(), name='publisher-detail'),
]
