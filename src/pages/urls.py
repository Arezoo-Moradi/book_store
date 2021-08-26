from django.urls import path, include

from .views import HomeView
from product.views import *
from accounts.views import *

urlpatterns = [
    path('',most_sell_book,name='home'),
    path('books/', HomeView.as_view(), name='books'),
    path('searched/', search_bar, name="search"),
    path('NewAdress/', create_address, name='NewAdress'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('orders/', history_orders, name='order'),
    path('<int:pk>/update_profile/', EditProfile.as_view(), name='update'),
    path('addresses/', list_address, name='addresses'),
    path('<int:pk>/update_address/', AddressEdit.as_view(), name='update_address'),
    path('home/', include('order.urls')),
    path('<int:pk>/delete_address/', delete_address, name='delete_address'),

]