from django.urls import path
from .views import *
from product.views import *


urlpatterns = [

    path('order-summary/', SummaryOfOrderView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='book_detail'),
    path('add-to-cart/<slug>/', add_to_shopping, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_of_shopping, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_item_shopping,
         name='remove-single-item-from-cart'),
    path('complete/', list_of_order, name='Complete'),
    path('address/', show_address, name='CH-ADD'),
    path('<int:pk>/record/', add_new_address, name='record'),


]
