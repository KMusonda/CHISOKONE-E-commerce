from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('become_vendor/', views.become_vendor, name='become_vendor'), #for becoming the vendor
    path('my_store/', views.my_store, name='my_store'),
    path('add-product/', views.add_product, name='add_product'),
]