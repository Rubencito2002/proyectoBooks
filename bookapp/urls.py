from django.urls import path
from . import views
from .views import BookList, BookDetail, BookCreate

urlpatterns = [
    path('', BookList.as_view(), name='book_list'),
    path('details', BookDetail.as_view(), name='book_list'),
    path('form', BookCreate.as_view(), name='book_form'),
]