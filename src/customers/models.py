from django.db import models
from django.contrib.auth.models import User, AnonymousUser

# class Customer(models.Model):
#     email = models.EmailField()
#     password = models.CharField(max_length=10)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=20)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    address = models.TextField(max_length=1000)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer}"


