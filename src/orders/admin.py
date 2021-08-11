from django.contrib import admin
from .models import *


# Register your models here.
# admin.site.register(Order_items)
# admin.site.register(Order)

@admin.register(Order_items)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_price')

    def get_title(self, obj):
        books = obj.book.all()

        return ",".join([str(book.title) for book in books])

    def get_price(self, obj):
        books = obj.book.all()

        lst_price = []
        for book in books:
            if float(book.price_discount) != 0:
                lst_price.append(float(book.price_discount))
            else:
                lst_price.append(float(book.price))
            total = sum(lst_price)

        obj.prices = total
        obj.save()
        return total


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_item', 'calculate_price', 'time')

    def calculate_price(self, obj):

        prices = float(obj.order_item.prices)

        dis = obj.discount
        if dis != None:
            disc=obj.discount.amount
            total = prices - prices * float(disc) / 100

        else:
            total = prices
        obj.total_price = total
        obj.save()
        return total
