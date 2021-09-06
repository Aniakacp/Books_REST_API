from django.urls import path

from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('books/', BookGenericView.as_view()),
    path('books/<int:id>/', BookGenericView.as_view()),
    path('filter3/', BookFilterView3.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])