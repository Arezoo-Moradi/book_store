from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    '''
        Category model

           name :   نام دسته
    '''
    name = models.CharField(verbose_name='دسته', max_length=100)

    class Meta:
        verbose_name_plural = 'دسته ها'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Book(models.Model):
    '''
        Book Model
            title:      عنوان کتاب
            author:       نویسنده
            inventory:   موجودی
            created:    زمان ایجاد
            price :        قیمت
            category :   دسته
            discount_price:    قیمت با تخفیف
            image:        تصویر
            slug:         اسلاگ
    '''

    title = models.CharField(verbose_name='عنوان ', max_length=100)
    price = models.FloatField(verbose_name='قیمت')
    author = models.CharField(verbose_name='نویسنده', max_length=100)
    inventory = models.IntegerField(verbose_name='موجودی')
    created = models.DateTimeField(verbose_name='زمان ایجاد', auto_now_add=True)
    discount_price = models.FloatField(verbose_name='قیمت با تخفیف', blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name='دسته')
    slug = models.SlugField(verbose_name='اسلاگ', blank=True)
    image = models.ImageField(verbose_name='تصویر', upload_to='book/', blank=True, null=True)
    num = models.IntegerField(default=0, blank=True, verbose_name='تعداد فروش')

    class Meta:
        verbose_name_plural = 'کتاب ها'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''
                Function for reverse to product page
        '''
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        '''
            This function reverse to add-to-cart
        '''
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        '''
            This function reverse to remove-from-cart
        '''
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })


class Discount(models.Model):
    '''
        Discount model

            type:            نوع تخفیف
            amount:          مقدار تخفیف
            list_books:     لیست کتاب ها
    '''

    TYPE_CHOICE = [('1', 'درصدی'), ('2', 'نقدی')]
    type = models.CharField(verbose_name='نوع تخفیف', max_length=20)
    amount = models.CharField(verbose_name='مقدار', max_length=20)
    list_books = models.ManyToManyField(Book, verbose_name='لیست کتاب ها', blank=True, related_name='list_books')

    class Meta:
        verbose_name_plural = 'تخفیف ها'
        ordering = ('amount',)

    def __str__(self):
        names = self.list_books.all()
        return ",".join([str(book.title) for book in names])

    def price_after_discount(self):
        '''
            This function, calculates the price of the book after applying the discount
        '''

        if self.type == 'درصدی':
            for book in self.list_books.all():
                book.discount_price = float(book.price)-float(book.price)*float(self.amount)/100
                book.save()
        else:
            # Cash discount
            for book in self.list_books.all():
                book.discount_price = float(book.price)-float(self.amount)