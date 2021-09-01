from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from product.models import *


class HomePageView(TemplateView):
    '''
        Home page view showing index templates
    '''

    template_name = 'books/index.html'


class HomeView(ListView):
    '''
        Home view displaying books
    '''

    model = Book
    paginate_by = 10
    template_name = "books/index.html"