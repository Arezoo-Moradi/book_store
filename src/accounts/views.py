from order.models import *
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from .forms import EditAddress
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from product.models import *
from django.views.generic.edit import UpdateView
from order.models import DiscountCode
from django.db.models import Q
from .models import *
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required


#customer

class ProfileView(TemplateView):
    template_name = 'customer/base.html'


@login_required()
def create_address(request):
    '''
        This function create address
    '''

    if request.method == 'POST':
        form = EditAddress(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_address = Address.objects.create(user=request.user, province=data['province'], city=data['city'],
                                                 postal_code=data['postal_code'], full_address=data['full_address'])
            new_address.save()
    else:
        form = EditAddress()

    return render(request, 'customer/address_new.html', {'form': form})


@login_required()
def history_of_orders(request):
    '''
        This function show history of order
    '''

    order = Order.objects.filter(user=request.user)
    context = {'order': order}
    return render(request, 'customer/order_history.html', context)


class EditProfile(UpdateView):
    '''
       Edit your profile
    '''

    model = CustomUser
    template_name = 'customer/edit_profile.html'
    fields = [
        "username", "email", "first_name", "last_name"]
    success_url = reverse_lazy('profile')


class AddressEdit(UpdateView):
    '''
        Edit your address
    '''
    model = Address
    template_name = 'customer/edit_address.html'
    fields = [
        "province", "city", "postal_code", "full_address"]
    success_url = reverse_lazy('profile')


def list_of_address(request):
    '''
        This function show list of address
    '''

    address = Address.objects.filter(user=request.user)
    context = {'addresses': address}
    return render(request, 'customer/list_address.html', context)


def delete_address(request, pk):
    '''
        This function delete a address
    '''

    Address.objects.filter(user=request.user, pk=pk).delete()
    return redirect("addresses")


#Staff

@staff_member_required()
def index(request):
    return render(request, 'staff/base.html', {})


def search_bar(request):
    '''
         This function, searched a book using title or author
    '''

    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(Q(title__contains=searched) | Q(author__contains=searched))
        context = {'searched': searched, 'books': books}
        return render(request, 'staff/search_bar.html', context)


class BookCreateView(CreateView):
    '''
        Create view for book
    '''

    model = Book
    template_name = 'staff/book_new.html'
    fields = ('title', 'author', 'category', 'price', 'inventory', 'image', 'slug')
    exclude = ('discount_price', 'created')
    success_url = "/Employees"


class BookView(ListView):
    '''
        Show Book
    '''

    model = Book
    paginate_by = 10
    template_name = "staff/list_book.html"


class BookUpdateView(UpdateView):
    '''
        Update view of book
    '''
    model = Book
    fields = [
        "title", 'author', 'price', 'inventory', 'category', 'discount_price', 'slug', 'image']
    success_url = "/Employees/listbook"


def delete_book(request, pk):
    '''
        This function delete a book
    '''

    Book.objects.filter(pk=pk).delete()
    return redirect("list_book")


def create_category(request):
    '''
        This function create  a category
    '''

    if request.method == "POST":
        name_cat = request.POST.get('name')
        sample = Category(name=name_cat)
        sample.save()
    cat_list = []
    cat_emp = []
    category_list = get_list_or_404(Category)
    for cat in category_list:
        task_cat = Book.objects.filter(category=cat)
        if task_cat.exists():
            cat_list.append(cat)
        else:
            cat_emp.append(cat)
    context = {'category_list1': cat_list, 'category_list0': cat_emp}
    return render(request, 'staff/category.html', context)


class CategoryView(ListView):
    '''
        view of category
    '''

    model = Category
    paginate_by = 10
    template_name = "staff/list_category.html"


class CategoryUpdateView(UpdateView):
    '''
        Update view of category
    '''

    model = Category
    fields = [
        "name"]
    success_url = "/Employees/listcat"


def delete_category(request, pk):
    '''
        This function delete a category
    '''

    Category.objects.filter(pk=pk).delete()
    return redirect("list_cat")


class DiscountCreateView(CreateView):
    '''
        Create a view for discount
    '''

    model = Discount
    template_name = 'staff/discount_new.html'
    fields = ('type', 'amount', 'list_books')
    success_url = "/Employees"


class DiscountView(ListView):
    '''
        View of discount
    '''

    model = Discount
    paginate_by = 10
    template_name = "staff/list_discount.html"


class DiscountUpdateView(UpdateView):
    '''
            Update view of discount
    '''

    model = Discount
    fields = [
        'type', 'amount', 'list_books']
    success_url = "/Employees/listdiscount"


def delete_discount(request, pk):
    '''
        This function delete a discount
    '''

    Discount.objects.filter(pk=pk).delete()
    return redirect("list_discount")


class DiscountCodeCreateView(CreateView):
    '''
        Create a view for discount code
    '''

    model = DiscountCode
    template_name = 'staff/discount_code_new.html'
    fields = ('code', 'amount', 'from_date', 'to_date')
    success_url = "/Employees"


class DiscountCodeView(ListView):
    '''
         View of discount code
    '''

    model = DiscountCode
    paginate_by = 10
    template_name = "staff/list_discount_code.html"


class DiscountCodeUpdateView(UpdateView):
    '''
        Update view of discount code
    '''

    model = DiscountCode
    fields = [
        'code', 'amount', 'from_date', 'to_date']
    success_url = "/Employees/listdiscountcode"


def delete_discount_code(request, pk):
    '''
            This function delete a discount code
    '''
    DiscountCode.objects.filter(pk=pk).delete()
    return redirect("list_discount_code")



