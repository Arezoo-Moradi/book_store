from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Order)
# admin.site.register(OrderItem)


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):

    list_display = ('code', 'from_date', 'to_date', 'amount')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'ordered_date', 'status', 'total_price')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('ordered', 'item', 'quantity', 'user')



