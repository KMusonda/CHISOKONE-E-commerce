from django.shortcuts import render

from store.models import Product

def frontpage(request): #this function is for the browser front page
    products = Product.objects.all()[:4]

    return render(request, 'core/frontpage.html', {
        'products': products
    })

def wallet(request): #this function is for the online wallet account
    return render(request, 'core/wallet.html')