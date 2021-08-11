from django.db import models


# Create your models here.

class Account(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=10)


class Staff(Account):
    fist_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    staff_code = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.fist_name} {self.last_name}"


