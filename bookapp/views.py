from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Book
from .forms import BookForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

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

class BookEdit(View):
    bookEdit_template = 'bookapp/book_edit.html'
    
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, self.bookEdit_template , {'book': book, 'form': form})
    
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, instance = book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('Book_List')
        return render(request, self.bookEdit_template , {'book': book, 'form': form})
"""

class BookList(ListView):
    model = Book

class BookDetail(DetailView):
    model = Book
    template_name = 'bookapp/book_details.html'

class BookEdit(UpdateView):
    model = Book
    fields = ["title", "author", "description", "rating"]
    template_name = 'bookapp/book_edit.html'
    success_url = reverse_lazy('Book_List')

class BookDelete(DeleteView):
    model = Book
    template_name = 'bookapp/book_delete.html'
    success_url = reverse_lazy('Book_List')

class BookCreate(View):
    books = Book.objects.all()
    bookForm_template = 'bookapp/book_form.html'

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