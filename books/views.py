from datetime import datetime
from urllib.request import urlopen
import json

import django_filters
from django.http import JsonResponse
from django.shortcuts import render

from django.views import View
from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser

from books.models import Book, Categories, Author
from books.serializers import BookSerializer
#from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

def retrieve_json(link):
    response = urlopen(link)
    return json.loads(response.read())

def update_upload(new_book, book):
    new_book.title = book['volumeInfo']['title']
    new_book.save()
    new_book.published_date = book['volumeInfo']['publishedDate']
    if 'averageRating' in book['volumeInfo']:
        new_book.average_rating = book['volumeInfo']['averageRating']
        new_book.save()
    if 'ratingsCount' in book['volumeInfo']:
        new_book.ratings_count = book['volumeInfo']['ratingsCount']
        new_book.save()
    if 'imageLinks' in book['volumeInfo']:
        new_book.thumbnail = book['volumeInfo']['imageLinks']['smallThumbnail']
    if 'authors' in book['volumeInfo']:
        for author in book['volumeInfo']['authors']:
            if not Author.objects.filter(name=author):
                Author.objects.create(name=author)
            new_book.authors.add(Author.objects.filter(name=author).last())
    if 'categories' in book['volumeInfo']:
        for cathegory in book['volumeInfo']['categories']:
            if not Categories.objects.filter(name=cathegory):
                Categories.objects.create(name=cathegory)
            new_book.categories.add(Categories.objects.filter(name=cathegory).last())
    new_book.save()

class BooksUploadView(View):
    def get(self, request):
        books = retrieve_json('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
        for book in books['items']:
            new_book= Book()
            update_upload(new_book, book)
        return render(request, 'books.html', {'books_list': Book.objects.all()})

class BooksUpdateView(View):
    def get(self, request):
        books = retrieve_json('https://www.googleapis.com/books/v1/volumes?q=war')
        new_book = Book.objects.all().first()
        for book in books['items']:
            update_upload(new_book, book)
            if (new_book.id + 1) <= Book.objects.all().last().id:
                new_book = Book.objects.get(id=new_book.id + 1)
        else:
            pass
        return render(request, 'books.html', {'books_list': Book.objects.all()})

class BookGenericView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
           return self.list(request)

    def post(self, request, id= None):
        return self.create(request)
    def put(self, request, id=None):
        return self.update(request, id)
    def delete(self, request, id):
        return self.destroy(request, id)

    def get_queryset(self):
        if self.request.query_params.get('published_date'):  #http://127.0.0.1:8000/books/?published_date=1995
            published_date= self.request.query_params.get('published_date')
            return Book.objects.filter(published_date=published_date)
        if self.request.query_params.get('author'):
            author = self.request.query_params.get('author')    #http://127.0.0.1:8000/books/?author=Rupert%20Furneaux&Tom%20Pendergast
            return Book.objects.filter(authors__name=author)    #http://127.0.0.1:8000/books/?author=Rupert%20Furneaux&author=Tom%20Pendergast
        if self.request.query_params.get('title'):
            title = self.request.query_params.get('title')    #http://127.0.0.1:8000/books/?author=Rupert%20Furneaux&Tom%20Pendergast
            return Book.objects.filter(title=title)    #http://127.0.0.1:8000/books/?author=Rupert%20Furneaux&author=Tom%20Pendergast
        if self.request.query_params.get('sort'):
            sort = self.request.query_params.get('sort')
            return Book.objects.all().order_by(f'{sort}') #http://127.0.0.1:8000/books/?sort=published_date
        else:
            return Book.objects.all()

class BookFilterView3(generics.ListAPIView):  #http://127.0.0.1:8000/filter3/?ordering=published_date
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends=(filters.SearchFilter, filters.OrderingFilter)
    search_fields=['published_date', 'title', 'authors__name']  #http://127.0.0.1:8000/filter3/?search=1995
                                                                #http://127.0.0.1:8000/filter3/?search=Tom%20Pendergast









