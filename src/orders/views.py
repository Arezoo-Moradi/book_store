from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *
from datetime import datetime


def get_order_item(request):
    
    '''
        add order item to shopping cart
    '''
    
    ords = Order_items.objects.all()
    ids = ords.values_list('pk', flat=True)
    # all id 
    ids = list(ids)
    bk = Order_items.objects.get(id=ids[0])
    books = bk.book.all()
    books = list(books)
    title = [book.title for book in books]
    price = [book.price for book in books]
    price_disc = []
    for book in books:
        if book.price_discount != '0':
            price_disc.append(book.price_discount)
        else:
            price_disc.append(book.price)
    bk.prices = 0
    for p in price_disc:
        bk.prices = bk.prices + float(p)
    bk.save()
    num = len(title)
    listzip = zip(title, price, price_disc)
    return render(request, 'books/order_items.html', {'listzip': listzip})


def remove_order_items(request, title):
    
    '''
        remove order item from shopping cart
    '''
    
    ords = Order_items.objects.all()
    ids = ords.values_list('pk', flat=True)
    # all id
    ids = list(ids)
    bk = Order_items.objects.get(id=ids[0])
    item = get_object_or_404(Book, title=title)
    bk.prices = float(bk.prices) - float(item.price)
    bk.book.remove(item)
    bk.save()
    return redirect(request.META['HTTP_REFERER'])


def send_order(request):
    '''
        send the order to order list
    '''
    ords = Order_items.objects.all()
    ids = ords.values_list('pk', flat=True)
    bk = Order_items.objects.get(id=ids[0])
    prices = float(bk.prices)
    total = prices
    total_discount = total
    times = datetime.now().date()
    order = Order.objects.create(
             time=times, order_item=bk, total_price=total, status='سفارش')

    order.get_book()

    if request.method == "POST":
        code = request.POST['code']
        code1 = DiscountCode.objects.filter(code=code)
        if code1.exists():
            today = datetime.now().date()
            first = code1[0].from_date
            final = code1[0].to_date
            # check the time of discount code
            if first < today < final:
                amt = float(code1[0].amount)
                total_discount = prices - prices * float(amt) / 100
                order.discount = code1[0]
                order.price_with_discount()
                order.save()
            else:
                messages.warning(request, 'کد نامعتبر است. ')
                return redirect(request.META['HTTP_REFERER'])

        else:
            messages.warning(request, 'کد ناموجود است. ')
            return redirect(request.META['HTTP_REFERER'])
    order_item = order.order_item
    # set the status to record
    status = order.status
    id = order.id
    context = {'order': order_item, 'total': total, 'discount': total_discount, 'status': status, 'id': id}
    return render(request, 'orders/orderlist.html', context)


# @login_required
def record_order(request, id):
    '''
       record the order
    '''
    order = get_object_or_404(Order, id=id)
    date_create = datetime.now().date()
    order.time = date_create
    order.status = 'record'
    order.save()
    bk = Order.objects.get(id=id)
    bk.status = 'ثبت'
    bk.save()
    order_item = order.order_item
    for item in order_item.book.all():
        book = Book.objects.filter(title=item)
        invent = int(book[0].inventory) - 1
        book.update(inventory=invent)
    context = {'status': bk.status, 'order': bk.books, 'prices': bk.total_price, 'time': bk.time}
    ords = Order_items.objects.all()
    ids = ords.values_list('pk', flat=True)
    bk = Order_items.objects.get(id=ids[0])
    bk.delete()
    return render(request, 'orders/finalrecord.html', context)