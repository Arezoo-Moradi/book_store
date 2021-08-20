from django.urls import path, include
from orders.views import *
from .views import *

urlpatterns = [
    path('', BookList.as_view(), name='index'),
    path('<int:pk>/detail/', BookDetail.as_view(),name='book_detail'),
    path('searched/', search_bar, name="search"),
    path('detail/<int:pk>', add_order, name='order-items'),
    path('orders/', get_order_item,name='orders'),
    path('compete/', send_order,name='Complete'),
    path('customer/', include('customers.urls')),
    path('delete/<str:title>', remove_order_items, name='delete'),
    path('record/<int:id>', record_order, name='record')

]