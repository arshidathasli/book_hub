from django.contrib import admin
from django.urls import path, include
from .views import AddBookView, SearchBooksView, UpdateBooksView, DeleteBooksView, BookListView, RetrieveBookView

urlpatterns = [
    path('add_book/', AddBookView.as_view(), name='signup'),
    path('search_book/', SearchBooksView.as_view(), name='search_book'),
    path('book/<int:pk>/', RetrieveBookView.as_view(), name='retrieve_book'),
    path('update_book/<int:pk>/', UpdateBooksView.as_view(), name='update_book'),
    path('delete_book/<int:book_id>/', DeleteBooksView.as_view(), name='delete_book'),

    path('booklist/', BookListView.as_view(), name='booklist'),

]
