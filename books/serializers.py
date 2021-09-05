from rest_framework import serializers

from books.models import Book, Author, Categories

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
     )
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    class Meta:
        model = Book
        fields = ('title', 'authors', 'published_date', 'categories', 'average_rating', 'ratings_count', 'thumbnail', 'authors')
        extra_kwargs = {'authors': {'required': False}}


