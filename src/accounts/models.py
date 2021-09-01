from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # add additional fields in here
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):
    '''
    Address model

            user:               کاربر
            province:           استان
            city:               شهر
            full_address:   آدرس کامل

    '''

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    province = models.CharField(verbose_name='استان', max_length=50)
    city = models.CharField(verbose_name='شهر', max_length=50)
    postal_code = models.BigIntegerField(verbose_name='کد پستی')
    full_address = models.TextField(verbose_name='آدرس کامل')

    class Meta:
        verbose_name_plural = 'آدرس ها'

    def __str__(self):
        return f"{self.province},{self.city},{self.full_address}"
