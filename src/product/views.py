from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import Q
from order.models import OrderItem


class HomeView(ListView):
    '''
            Show book
    '''

    model = Book
    template_name = "books/lst.html"


class ItemDetailView(DetailView):
    '''
            Show detail of book
    '''
    model = Book
    template_name = "books/book-detail.html"


def search_bar(request):
    '''
            This function, searched a book using title or author
    '''

    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(Q(title__contains=searched) | Q(author__contains=searched))
        context = {'searched': searched, 'books': books}
        return render(request, 'books/search_bar.html', context)


def best_sellers(request):
    '''
            This function, displaying bestsellers book
    '''

    dic_book = {}
    best_sell_book = []
    books = Book.objects.all()
    for book in books:
        dic_book[book.title] = book.num
    dic_book = dict(sorted(dic_book.items(), key=lambda item: item[1], reverse=True))
    f = list(dic_book.keys())
    for i in range(3):
        b = Book.objects.filter(title=f[i])
        best_sell_book.append(b[0])
    return render(request, 'books/index.html', {'title': best_sell_book})




