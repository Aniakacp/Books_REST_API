from django.db import models

class Author(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    title= models.CharField(max_length=500)
    authors= models.ManyToManyField(Author)
    published_date= models.CharField(max_length=10, blank=True)
    categories= models.ManyToManyField(Categories)
    average_rating= models.DecimalField(max_digits=2, decimal_places=1, null=True)
    ratings_count= models.SmallIntegerField(null=True)
    thumbnail = models.CharField(max_length=500, blank=True)
