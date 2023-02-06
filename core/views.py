from django.shortcuts import render

from store.models import Product, Category

def frontpage(request): #this function is for the browser front page
    products = Product.objects.filter(status=Product.ACTIVE).order_by('?')
    category = Category.objects.all()

    return render(request, 'core/frontpage.html', {
        'products': products,
        'category': category,
    })

def wallet(request): #this function is for the online wallet account
    return render(request, 'core/wallet.html')