from django.shortcuts import render, redirect
from django.views import View
from .models import Book
from django.forms import BookForm

class BookList(View):
    bookList_template = 'book/book_list.html'
    def get(self, request):
        books = Book.objects.all()
        return render(request, self.bookList_template , {'books': Book})

class BookDetail(View):
    bookDetail_template = 'book/book_detail.html'
    def get(self, request, id):
        books = Book.objects.get(id=id)
        return render(request, self.bookDetail_template , {'books': Book})

class BookCreate(View):
    bookForm_template = 'book/book_form.html'
    def get(self, request):
        form = BookForm()
        return render(request, self.bookForm_template , {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        return render(request, self.bookForm_template , {'form': form})