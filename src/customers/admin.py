from django.contrib import admin
from .models import *

admin.site.register(Address)

class AddressAdmin(admin.TabularInline):
    model = Address


# class CustomerAdmin(admin.ModelAdmin):
#     inlines = [AddressAdmin, ]
#     list_display = ('last_name', 'first_name', 'created', 'get_address',)
#
#     def get_address(self, obj):
#         adr = Address.objects.filter(customer=obj.id)
#         add = []
#         for ad in adr:
#             add.append(ad.address)
#         return add
#
#
# admin.site.register(CustomerAdmin)
