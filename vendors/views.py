from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.text import slugify

from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect

from .models import Vendor

from store.models import Product
from store.forms import ProductForm

def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'vendors/become_vendor.html', {'form': form})

def my_store(request):
    products = request.vendor.products.exclude(status=Product.DELETED)

    return render (request, 'vendors/my_store.html', {
        'products':products
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')

            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'the product was added.')

            return redirect('my_store')
    else:
        form = ProductForm()

    return render(request, 'vendors/product_form.html', {
        'title': 'add product',
        'form': form
    })
        