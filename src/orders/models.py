from django.db import models
from books.models import *
from discounts.models import *
from customers.models import *
from django.contrib.auth.models import User, AnonymousUser


class Order_items(models.Model):
    book = models.ManyToManyField(Book, blank=True)
    prices = models.CharField(max_length=20, default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        books = self.book.all()
        return ",".join([str(book.title) for book in books])


class Order(models.Model):
    STATUS_CHOICE = [('order', 'سفارش'), ('record', 'ثبت')]
    total_price = models.CharField(max_length=20, blank=True, default=0)
    time = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=10)
    order_item = models.ForeignKey(Order_items, on_delete=models.SET_NULL, null=True)
    books = models.CharField(max_length=500, blank=True)
    discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', null=True, blank=True, on_delete=models.CASCADE
                             , default=AnonymousUser.id)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def get_book(self):
        lst = self.order_item.book.all()
        print(lst)
        self.books = lst[0].title
        self.save()
        return self.books

    def price_with_discount(self):
        code = self.discount
        amt = code.amount
        self.total_price = float(self.total_price) - float(self.total_price) * (float(amt)) / 100
        self.save()
        return self.total_price

    def __str__(self):
        return f"{self.user},{self.status}"
