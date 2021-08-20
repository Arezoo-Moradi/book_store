from django.db import models

# from discounts.models import *


# Create your models here.
from django.urls import reverse


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
    image = models.ImageField(blank=True)

    def get_add_to_order_url(self):
        return reverse("order-items", kwargs={
            'pk': self.id
        })

    def __str__(self):
        return self.title
