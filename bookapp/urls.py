from django.urls import path
from . import views
from .views import Book_List, Book_Detail, Book_Create

urlpatterns = [
    path('', Book_List.as_view(), name='book_list'),
    path('details', Book_Detail.as_view(), name='book_list'),
    path('form', Book_Create.as_view(), name='book_form'),
]