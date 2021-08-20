from django.urls import path
from customers import views as user_view
from django.contrib.auth import views as auth
from .views import *
urlpatterns = [
    path('login/', user_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='customer/index.html'), name='logout'),
    path('register/', user_view.register, name='register')
]