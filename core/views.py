from django.shortcuts import render

from store.models import Product, Category
from userprofile.models import Userprofile

def frontpage(request): #this function is for the browser front page
    products = Product.objects.exclude(status=Product.DELETED).order_by('?') [:4]#here we can filter types of products to be rendered on the front page by writing (status=Product.ACTIVE)
    category = Category.objects.all()
    products_slider = Product.objects.filter(status=Product.ACTIVE).order_by('id')[:4] #first 3 products
    products_latest = Product.objects.filter(status=Product.ACTIVE).order_by('-id')[:3] #last 3 products
    vendors = Userprofile.objects.all().order_by('?')[:3] #random selected products

    return render(request, 'core/frontpage.html', {
        'products': products,
        'category': category,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'vendors': vendors,
    })

def wallet(request): #this function is for the online wallet account
    return render(request, 'core/wallet.html')

def about(request): #this function is for the online wallet account
    return render(request, 'core/about.html')