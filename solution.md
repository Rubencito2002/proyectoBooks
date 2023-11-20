# Pasos a seguir para la creaccion de nuestro proyecto:

## Paso 1: Instalacion de lo necesario:
Para este proyecto necesitaremos realizar lo siguinte:
```bash
    # Creaccion del entorno virtual.
    mkvirtualenv pruebaDjango

    # Para actualizar los repositorios.
    python -m pip install --upgrade pip

    # Ejecucion del fichero requirements
    pip install -r requirements.txt
```

Para el fichero requirements.txt pondremos lo siguiente:

```text
    Django~=4.2.7
```

## Paso 2: Creaccion de nuestro proyecto:

```bash
    # Para crear los archivos y directorios.
    django-admin startproject book .
```

## Paso 3: Configuración Básica de nuestro proyecto:
Ahora configuraremos el fichero que esta ubicando en book/settings.py y le cambiaremos lo siguinte:

```python
    TIME_ZONE = 'Europe/Madrid'
    LANGUAGE_CODE = 'es-es'
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'
    ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']
```

Tambien configuraremos la base de datos de nuestro proyecto con lo siguiente en el mismo fichero anterior:

```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Despues de añadir lo de la base de datos tendremos que ejecutar lo siguiente en la terminal:

```bash
    # Para generar el fichero de la base de datos.
    python manage.py migrate
```

Despues de esta configuración ejecutaremos el siguiente comando para probar en el navegador nuestro proyecto en funcionamiento.

```bash
    python manage.py runserver
```

En el navegador pondremos lo siguiente para probar que funciona todo bien:
```text
    * Opción 1:
    localhost:8000
    * Opción 2:
    127.0.0.1:8000
```

## Paso 4: Creacción de Modelo.
Para la creación de nuestra aplicacion de tarea ejecutaremos lo siguiente en la terminal:
```bash
    # Para la creacion de nuestra aplicacion de tarea.
    python manage.py startapp bookapp
```

Despues configuraremos lo siguiente en el fichero mysite/settings.py

```python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookapp',
]
```

Ahora configuraremos el fichero de modelo en la carpeta de bookapp. Que lo que pondremos en ese fichero sera lo siguiente:
```python
    from django.contrib.auth.models import User
    from django.core.validators import MaxValueValidator
    from django.db import models
    from django.db.models import Model, CASCADE

    class Book(models.Model):
        title = models.CharField(max_length=150)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        description = models.CharField(max_length=500)
        rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title
```

Despues de añadir en fichero lo anterior tendremos que ejecutar lo siguiente en la terminal:

```bash
    # Para preparar los ficheros para migrarlo a la base de datos.
    python manage.py makemigrations bookapp

    # Django preparó un archivo de migración que ahora tenemos que aplicar a nuestra base de datos.
    python manage.py migrate bookapp
```
## Paso 5: Administracción de Django.
Abre el fichero bookapp/admin.py en el editor y reemplaza su contenido con esto:
```python
    from django.contrib import admin
    from .models import Book

    admin.site.register(Book)
```

Despues de añadir lo anterior en el fichero indicado tendremos que ejecutar lo siguiente en la terminal:
```bash
    # Creaccion del usuario.
    python manage.py createsuperuser
```

## Paso 6: Configuración de las Urls.
Para la configuración de las urls de nuestro proyecto tendremos que modificar lo siguiente:
```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('bookapp.urls'))
]
```

Crea un nuevo fichero vacío llamado urls.py en el directorio bookapp para añadir lo siguiente en el fichero:
```python
    from django.urls import path
    from . import views
    from .views import BookList, BookDetail, BookCreate, BookEdit

    urlpatterns = [
        path('', BookList.as_view(), name='Book_List'),
        path('details/<int:pk>', BookDetail.as_view(), name='Book_Details'),
        path('formulario/', BookCreate.as_view(), name='Book_Create'),
        path('edit/<int:pk>/', BookEdit.as_view(), name='Book_Edit'),
    ]
```

## Paso 7: Creacción del formulario.
Ahora crearemos el fichero forms.py de la carpeta bookapp que pondremos lo siguiete:
```python
    from django import forms
    from  .models import Book

    class BookForm(forms.ModelForm):
        class Meta:
            model = Book
            fields = ['title', 'author', 'description', 'rating']
```

## Paso 8: Creacción de las vistas.
Ahora configuraremos el fichero views.py de la carpeta bookapp que pondremos lo siguiete:
```python
    from django.shortcuts import get_object_or_404, render, redirect
    from django.views import View
    from .models import Book
    from .forms import BookForm
    from django.views.generic import ListView, DetailView

    class BookList(ListView):
    model = Book

    class BookDetail(DetailView):
        model = Book
        template_name = 'bookapp/book_details.html'

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
```

## Paso 9: Creacción de plantillas.
Ahora crearemos en la carpeta de bookapp un nuevo directorio llamado templates y dentro de ella crearemos otra carpeta llamada booapp.
Dentro de esta carpeta crearemos nuestra primera plantilla con el siguiente nombre base.html, dentro del fichero pondremos lo siguiente:
```text
    <!DOCTYPE html>
    <html lang="es" data-theme="light">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.classless.min.css">
        </head>
        <body>
            <header>
                <nav>
                    <ul>
                        <li><strong>Book Store</strong></li>
                    </ul>
                    <ul>
                        <li><a href="{% url 'Book_List' %}" role="button">Listado de Libros</a></li>
                        <li><a href="{% url 'Book_Create' %}" role="button">Nuevo Libro</a></li>
                    </ul>
                </nav>
            </header>

            <main>
                {% block content %}{% endblock %}
            </main>
        </body>
    </html>
```

Despues crearemos varios ficheros respecto a cada vista que hemos creado que son los siguientes (todos ellos extendiento sobre el fichero base.html):
Primera vista es el listado de libros y el nombre del fichero es book_list.html con el siguiente contenido:
```text
    {% extends 'bookapp/base.html' %}
    {% block content %}
        <h1>Listado de Libros</h1>
        {% for book in object_list %}
            <article>    
                <p> {{ book.title }} </p>
                <a href="{% url 'Book_Details' pk=book.pk %}" role="button">Detalles</a>    
            </article>
        {% endfor %}
    {% endblock %}
```

Segunda vista son los detalles de un  libro y el nombre del fichero es book_details.html con el siguiente contenido:
```text
    {% extends 'bookapp/base.html' %}
    {% block content %}
        <h2>Detalles del Libro</h2>
        <article>
            <p><strong>Título:</strong> {{ book.title }}</p>
            <p><strong>Autor:</strong> {{ book.author }}</p>
            <p><strong>Descripción:</strong> {{ book.description }}</p>
            <p><strong>Rating:</strong> {{ book.rating }}</p>
            <a href="{% url 'Book_Edit' pk=book.pk %}" role="button">Editar libro</a>
        </article>
    {% endblock %}
```

Tercero vista es el formulario de libros y el nombre del fichero es book_form.html con el siguiente contenido:
```text
    {% extends 'bookapp/base.html' %}
    {% block content %}
        <h2>Añadir Libro</h2>
        <form action="{% url 'Book_Create' %}" method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Nueva Libro</button>
        </form>
    {% endblock %}
```

Cuarta vista es el editado de un libro y el nombre del fichero es book_edit.html con el siguiente contenido:
```text
    {% extends 'bookapp/base.html' %}
    {% block content %}
        <h2>Añadir Libro</h2>
        <form action="{% url 'Book_Edit' pk=book.pk %}" method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Libro Editado</button>
        </form>
    {% endblock %}
```