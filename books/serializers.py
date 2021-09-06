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
        queryset=Author.objects.all(),
        slug_field='name',
     )
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Categories.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Book
        fields = ('title', 'authors', 'published_date', 'categories', 'average_rating', 'ratings_count', 'thumbnail', 'authors')
        extra_kwargs = {'authors': {'required': False}}

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        categories_data = validated_data.pop('categories')
        book = Book.objects.create(**validated_data)
        for author in authors_data:
            Author.objects.create(**author)
            #book.authors.add(author)
        return book


    def update(self, instance, validated_data):
        if validated_data.get('authors'):
            authors_data = validated_data.get('authors')
            authors_serializer = AuthorSerializer(data=authors_data)

            if authors_serializer.is_valid():
                authors = authors_serializer.update(instance=instance.authors,
                                                    validated_data=authors_serializer.validated_data)
                validated_data['authors'] = authors
        if validated_data.get('categories'):
            categories_data = validated_data.get('categories')
            categories_serializer = CategoriesSerializer(data=categories_data)

            if categories_serializer.is_valid():
                categories = categories_serializer.update(instance=instance.categories,
                                                    validated_data=categories_serializer.validated_data)
                validated_data['categories'] = categories

        return super().update(instance, validated_data)


