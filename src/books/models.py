from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    inventory = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    price = models.CharField(max_length=10)
    categories = models.ManyToManyField(Category)
    price_discount = models.CharField(max_length=20, default=0, blank=True)

    def __str__(self):
        return self.title

