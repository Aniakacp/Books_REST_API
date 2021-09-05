from django.urls import path, include

from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import *
from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter

#class BookListView2(viewsets.ModelViewSet):
 #   serializer_class = BookSerializer
 #   queryset = Book.objects.all()

#router= DefaultRouter()
#router.register('article', BookListView2, basename='article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', BooksUploadView.as_view()),
    path('update/', BooksUpdateView.as_view()),
    path('books/', BookGenericView.as_view()),
    path('books/<int:id>/', BookGenericView.as_view()),
    path('filter3/', BookFilterView3.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])