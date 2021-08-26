from django.contrib import admin
from .models import *
from django.contrib import admin
from .models import *


# Register your models here.
# admin.site.register(Book)
admin.site.register(Category)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'inventory', 'discount_price')
    search_fields = ['title','author']
    list_filter = ("title", "author", "inventory")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('type', 'get_title', 'amount', 'get_price', 'get_price_discount')

    def get_title(self, obj):
        '''
            This function, get the title of book
        '''

        books = obj.list_books.all()
        return ",".join([str(book.title) for book in books])

    def get_price(self, obj):
        '''
            This function, get the price of book
        '''

        books = obj.list_books.all()
        return [book.price for book in books]

    def get_price_discount(self, obj):
        '''
            This function, receives a discounted book price
        '''

        books = obj.list_books.all()
        for book in books:
            if obj.type =='درصدی ':
                print(book)
                total_price = float(book.price)-(float(book.price)*float(obj.amount)/100)
            else:
                # Cash discount
                total_price = float(book.price)-float(obj.amount)
            book.discount_price = total_price
            book.save()

            return book.discount_price

