from django.shortcuts import render, redirect
from django.views import View
from .models import Book
from .forms import BookForm
from django.views.generic import ListView, DetailView

"""
class BookList(View):
    nombre_template = 'book/book_list.html'

    def get(self,request):
        books = Book.objects.all()
        form = BookForm()
        return render(request, self.nombre_template, {'books': books})

class BookDetail(View):
    bookDetail_template = 'book/book_details.html'

    def get(self, request, id):
        books = Book.objects.get(id=id)
        return render(request, self.bookDetail_template , {'books': books})
"""

class BookList(ListView):
    model = Book

class BookDetail(DetailView):
    model = Book
    bookDetail_template = 'book/book_details.html'

class BookCreate(View):
    books = Book.objects.all()
    bookForm_template = 'book/book_form.html'

    def actualizarBook(self):
        self.books = Book.objects.all()
        return self.books
    
    def get(self, request):
        books = Book.objects.all()
        form = BookForm()
        return render(request, self.bookForm_template , {'books': self.actualizarBook, 'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Book_List')
        books = Book.objects.all()
        return render(request, self.bookForm_template , {'books': self.actualizarBook, 'form': form})