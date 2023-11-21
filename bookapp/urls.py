from django.urls import path
from . import views
from .views import BookList, BookDetail, BookCreate, BookEdit, BookDelete

urlpatterns = [
    path('', BookList.as_view(), name='Book_List'),
    path('details/<int:pk>', BookDetail.as_view(), name='Book_Details'),
    path('formulario/', BookCreate.as_view(), name='Book_Create'),
    path('edit/<int:pk>/', BookEdit.as_view(), name='Book_Edit'),
    path('delete/<int:pk>/', BookDelete.as_view(), name='Book_Delete')
]