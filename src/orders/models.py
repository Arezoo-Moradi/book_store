from django.db import models
from books.models import *
from discounts.models import *
from customers.models import *


class Order_items(models.Model):
    book = models.ManyToManyField(Book, blank=True)
    prices = models.CharField(max_length=20, default=0)

    def __str__(self):
        books = self.book.all()
        return ",".join([str(book.title) for book in books])


class Order(models.Model):
    STATUS_CHOICE = [('order', 'سفارش'), ('record', 'ثبت')]
    total_price = models.CharField(max_length=20, blank=True, default=0)
    time = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=10)
    order_item = models.ForeignKey(Order_items, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer},{self.order_item},{self.status}"


