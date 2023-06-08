### this form is for vendors to add products in the store

from django import forms

from.models import Product, Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'keywords', 'description', 'image', 'price', 'variant', 'detail', 'status',)