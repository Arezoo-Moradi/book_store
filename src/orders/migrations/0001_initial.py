# Generated by Django 3.2.6 on 2021-08-11 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('books', '0001_initial'),
        ('discounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prices', models.CharField(default=0, max_length=20)),
                ('book', models.ManyToManyField(blank=True, to='books.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.CharField(blank=True, default=0, max_length=20)),
                ('time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('order', 'سفارش'), ('record', 'ثبت')], max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('discount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='discounts.discountcode')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order_items')),
            ],
        ),
    ]
