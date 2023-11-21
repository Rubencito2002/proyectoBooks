from django import forms
from  .models import Book
from django.forms import modelformset_factory

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'rating']

BookFormSet = modelformset_factory(Book, form=BookForm, extra=2, max_num=1)