from django.urls import path, include
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('searched/', search_bar, name="search"),
    path('NewBook/', BookCreateView.as_view(),name='NewBook'),
    path('listbook/', BookView.as_view(), name='list_book'),
    path('<int:pk>/update_book', BookUpdateView.as_view(), name='update_book'),
    path('<int:pk>/delete_book/', delete_book, name='delete_book'),
    path('Category/', create_category, name='Category'),
    path('<int:pk>/update', CategoryUpdateView.as_view(), name='update_cat'),
    path('listcat/', CategoryView.as_view(), name='list_cat'),
    path('<int:pk>/delete/', delete_category, name='delete'),
    path('NewDiscount/', DiscountCreateView.as_view(), name='NewDiscount'),
    path('listdiscount/', DiscountView.as_view(),name='list_discount'),
    path('<int:pk>/update_discount', DiscountUpdateView.as_view(),name='update_discount'),
    path('<int:pk>/delete_discount/', delete_discount,name='delete_discount'),
    path('NewDiscountCode/', DiscountCodeCreateView.as_view(), name='NewDiscountCode'),
    path('listdiscountcode/', DiscountCodeView.as_view(), name='list_discount_code'),
    path('<int:pk>/update_discount_code', DiscountCodeUpdateView.as_view(), name='update_discount_code'),
    path('<int:pk>/delete_discount_code/', delete_discount_code, name='delete_discount_code'),

]