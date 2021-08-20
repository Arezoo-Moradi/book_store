from django.contrib import admin
from .models import *

admin.site.register(DiscountCode)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('type', 'get_title', 'amount', 'get_price', 'get_price_discount')

    def get_title(self, obj):
        books = obj.list_books.all()
        return ",".join([str(book.title) for book in books])

    def get_price(self, obj):
        books = obj.list_books.all()
        return [book.price for book in books]

    def get_price_discount(self, obj):
        books = obj.list_books.all()
        total_price = 0
        for book in books:
            if obj.type =='درصدی' :
                print(book)
                total_price = float(book.price)-(float(book.price)*float(obj.amount)/100)+total_price
            else:
                total_price = float(book.price)-float(obj.amount)+total_price
            book.price_discount = total_price
            book.save()

            return book.price_discount

