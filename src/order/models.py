from django.conf import settings
from django.db import models
from product.models import Book
from accounts.models import CustomUser, Address

# Create your models here.


class DiscountCode(models.Model):
    '''
    Discount Code model

            code:       کد تخفیف
            from_date:   از تاریخ
            to_date:     تا تاریخ
            amount:        مقدار
    '''

    code = models.CharField(verbose_name='کد تخفیف', max_length=20)
    from_date = models.DateField(verbose_name='از تاریخ')
    to_date = models.DateField(verbose_name=' تا تاریخ')
    amount = models.CharField(verbose_name='مقدار', max_length=20)

    class Meta:
        verbose_name_plural = 'تخفیف امتیازی'
        ordering = ('amount',)

    def __str__(self):
        return self.code


class OrderItem(models.Model):
    """
     OrderItem model

           ordered:  سفارش
           item:    کتاب مورد نظر
           quantity: تعداد
           user:     کاربر
    """

    ordered = models.BooleanField(verbose_name='سفارش', default=False)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='موجودی', default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'جزئیات سفارش'

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        '''
            This function, returns the price of the selected books
        '''

        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        '''
            This function, applies discount to the quantity of item
        '''

        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        '''
            This function saves amount
        '''
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        '''
            This function, returns final price
        '''

        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    '''
    Order model

            item:        جزئیات سفارش
            start_date:   زمان ایجاد سفارش
            ordered_date:  'تاریخ ثبت سفارش
            status:       وضعیت سفارش
            address:        آدرس
            discount:       تخفیف
            total_price:    قیمت کل
            user:             کاربر

    '''

    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(verbose_name='زمان ایجاد سفارش', auto_now_add=True)
    ordered_date = models.DateTimeField(verbose_name='تاریخ ثبت سفارش')
    status = models.BooleanField(verbose_name='وضعیت سفارش', default=False)
    address = models.ForeignKey(Address, related_name='address',
                                on_delete=models.SET_NULL, blank=True, null=True)
    discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    total_price = models.CharField(verbose_name='قیمت کل', max_length=100, default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'سفارش ها'
        ordering = ['start_date']

    def __str__(self):
        return self.user.username

    def get_total(self, code):

        '''
            This function, returns the total price
        '''

        total = 0
        self.discount = code
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.discount:
            total = float(total) - float(total) * float(self.discount.amount) / 100
        self.total_price = total
        self.save()
        return total

    def get_title_of_book(self):

        '''
            This function, returns the title of book
        '''

        books = self.items.all()
        ITEMS = {}

        for book in books:
            b = str(book).split('of')
            ITEMS[b[1]] = b[0]

        return ITEMS

    def inventory_book(self):
        '''
            This function, returns the inventory of book
        '''

        items = self.items.all()

        for i in items:
            book = i.item
            book.inventory -= i.quantity
            book.num += i.quantity
            book.save()












