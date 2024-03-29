import json
import stripe

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Images, Order, OrderItem

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')

def success(request):
    return render(request, 'store/success.html')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    
    return redirect('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'cart': cart
    })

@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderForm(request.POST)

        total_price = 0
        items = []

        for item in cart:
            product = item['product']
            commission = (product.price * int(item['quantity'])) * 0.02
            total_price += (product.price * int(item['quantity']) + commission) / 100

            items.append({
                'price_data': {
                    'currency': 'zmw',
                    'product_data': {
                        'name': product.title,
                    },
                    'unit_amount': product.price
                },
                'quantity': item['quantity']
            })

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/success/',
            cancel_url='http://127.0.0.1:8000/cart/',
        )
        payment_intent = session.payment_intent

        order = Order.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=['phone'],
            address=data['address'],
            city=['city'],
            created_by = request.user,
            is_paid = True,
            payment_intent = payment_intent,
            paid_amount = total_price
        )

        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity

            item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
        cart.clear()
        
        return JsonResponse({'session': session, 'order': payment_intent})
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    })

def search(request):
    query = request.GET.get('query', '') # status=Product.ACTIVE to show only active products in the search page
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html', {
        'query': query,
        'products': products,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.exclude(status=Product.DELETED)# status=Product.ACTIVE to show only active products in the category detail page

    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)# status=Product.ACTIVE to show only active products in the product detail page
    category = get_object_or_404(Category, slug=category_slug)
    images = Images.objects.filter()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'category': category,
        'images': images,
    })
