from django.db import models

# Create your models here.
from books.models import Book


class Discount(models.Model):
    TYPE_CHOICE = [('1', 'درصدی'), ('2', 'نقدی')]
    type = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)
    list_books = models.ManyToManyField(Book, blank=True, related_name='list_books')

    def __str__(self):
        names = self.list_books.all()
        return ",".join([str(book.title) for book in names])


class DiscountCode(models.Model):
    type = 'امتیازی'
    code = models.CharField(max_length=20)
    from_date = models.DateField()
    to_date = models.DateField()
    amount = models.CharField(max_length=20)

    def __str__(self):
        return self.code