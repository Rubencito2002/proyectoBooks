from django.urls import path
from . import views
from .views import BookList, BookDetail, BookCreate

urlpatterns = [
    path('', BookList.as_view(), name='Book_List'),
    path('details/<int:pk>', BookDetail.as_view(), name='Book_Details'),
    path('formulario/', BookCreate.as_view(), name='Book_Create'),
]