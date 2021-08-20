from django.contrib import messages
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from orders.models import *
from .models import *


# Create your views here.

class BookList(ListView):
    model = Book
    template_name = 'books/index.html'


class BookDetail(DetailView):
    model = Book
    template_name = 'books/book-detail.html'


def search_bar(request):
    '''
        searched a book using title or author
    '''
    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(Q(title__contains=searched) | Q(author__contains=searched))
        context = {'searched': searched, 'books': books}
        return render(request, 'books/search_bar.html', context)


def add_order(request, pk):
    '''
        add book to order
    '''

    ords = Order_items.objects.all()
    # values_list similar a queryset
    ids = ords.values_list('pk', flat=True)
    # all id
    ids = list(ids)
    if ords.exists():
        b = Order_items.objects.get(id=ids[0])
        item = get_object_or_404(Book, pk=pk)

        # check the store of book
        if item.inventory > 0:
            if item.price_discount != 0:
                p = item.price_discount
            else:
                p = item.price
            name = item.title
            book = Book.objects.filter(title=name).get(title=name)
            b.book.add(book)
            b.quantity += 1
            b.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.warning(request, "ناموجود است.")
            return redirect(request.META['HTTP_REFERER'])

    else:
        item = get_object_or_404(Book, pk=pk)
        if item.inventory > 0:
            if item.price_discount != 0:
                p = item.price_discount
            else:
                p = item.price
            name = item.title
            book = Book.objects.filter(title=name)
            print(book)
            order_items = Order_items.objects.create(prices=p)
            order_items.book.set(book)
            order_items.quantity += 1
            order_items.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.warning(request, "ناموجود است.")
            return redirect(request.META['HTTP_REFERER'])







