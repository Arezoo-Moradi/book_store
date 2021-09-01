from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['province', 'city', 'postal_code']


admin.site.register(CustomUser, CustomUserAdmin)




