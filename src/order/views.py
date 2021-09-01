from datetime import datetime

from django.utils import timezone
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views.generic.base import View
from .models import *
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


class SummaryOfOrderView(LoginRequiredMixin, View):
    '''
        Summary of order
    '''

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, status=False)
            context = {
                'object': order
            }
            return render(self.request, 'books/order_items.html', context)

        except:
            messages.warning(self.request, "You do not have an active order")
            context = {}
            return render(self.request, 'books/order_items.html', context)


@login_required
def add_to_shopping(request, slug):
    '''
        This function, add item to shopping basket
    '''
    item = get_object_or_404(Book, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, status=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the inventory of the item exist
        if item.inventory > 0:
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "تعداد آیتم ها آپدیت شد.")
                return redirect("order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "آیتم مورد نظر به سبد خرید اضافه شد.")
                return redirect("order-summary")
        else:
            messages.warning(request, "ناموجود است.")
            return redirect(request.META['HTTP_REFERER'])

    else:
        if item.inventory > 0:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "کتاب موردنظر به سبد افزوده شد.")
            return redirect("order-summary")
        else:
            messages.warning(request, "ناموجود است.")
            return redirect(request.META['HTTP_REFERER'])


@login_required
def remove_of_shopping(request, slug):
    '''
        This function, remove item from shopping basket
    '''
    item = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        status=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "آیتم مورد نظر از سبد خرید حذف شد.")
            return redirect("order-summary")
        else:
            messages.info(request, "این آیتم در سبد خرید نیست.")
            return redirect("product", slug=slug)
    else:
        messages.info(request, " سفارش فعال ندارید.")
        return redirect("product", slug=slug)


@login_required
def remove_item_shopping(request, slug):
    '''
        This function, remove item using the mark -  from shopping basket
    '''

    item = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        status=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "تعداد آیتم ها آپدیت شد.")
            return redirect("order-summary")
        else:
            messages.info(request, "این آیتم در سبد خرید نیست. ")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "سفارش فعال ندارید. ")
        return redirect("product", slug=slug)


def list_of_order(request):
    '''
        This function, return list of order
    '''

    order = Order.objects.filter(user=request.user, status=False)
    orderitem = order[0].get_title_of_book()
    total = 0
    status = order[0].status
    id = order[0].id
    t = 0
    title = []
    for k in orderitem.keys():
        t = t + int(orderitem[k])
        title.append(k)
    if request.method == "POST":
        code = request.POST['code']
        code1 = DiscountCode.objects.filter(code=code)
        if code1.exists():
            today = datetime.now().date()
            first = code1[0].from_date
            final = code1[0].to_date
            if first < today < final:
                total_discount = order[0].get_total(code1[0])

            else:
                messages.warning(request, 'نا معتبر ')
        else:
            messages.warning(request, 'کد اشتباه است ')

    else:
        for order_item in order[0].items.all():
            total += order_item.get_final_price()
        ord = Order.objects.get(id=order[0].id)
        print(total)
        total_discount = total
        ord.total_price = total
        ord.save()

    context = {'order': title, 'quantity': t, 'total': total, 'discount': total_discount, 'status': status, 'id': id}
    return render(request, 'order/orderlist.html', context)


def show_address(request):
    '''
        This function show the page of address
    '''

    if request.method == "POST":
        province = request.POST.get('province')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        full_address = request.POST.get('full_address')
        new_add = Address(user=request.user, province=province, city=city, postal_code=postal_code,
                          full_address=full_address)
        new_add.save()
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses': addresses}
    return render(request, 'order/address.html', context)


def add_new_address(request, pk):
        '''
            This function could add new address or chose old address
        '''

        order = Order.objects.filter(user=request.user, status=False)
        ord = Order.objects.get(id=order[0].id)
        ord.inventory_book()
        items = ord.items.all()
        for item in items:
            item.ordered = True
            item.save()
        total = order[0].total_price
        time = order[0].ordered_date
        id = order[0].pk
        add = Address.objects.filter(user=request.user, pk=pk)
        ord.address = add[0]
        ord.status = True
        status = True
        address = add[0]
        ord.save()

        context = {'order': id, 'address': address, 'total': total,
                   'status': status, 'time': time}

        return render(request, 'order/finalrecord.html', context)
