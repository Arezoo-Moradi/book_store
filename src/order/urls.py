from django.urls import path
from .views import *
from product.views import *


urlpatterns = [

    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='book_detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('complete/', order_list, name='Complete'),
    path('address/', choice_address, name='CH-ADD'),
    path('<int:pk>/record/', choice_address_2, name='record'),


]
