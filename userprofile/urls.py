from django.contrib.auth import views as auth_views
from django.urls import path
from core import views as core_views

from . import views

urlpatterns = [
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('register', views.register_request, name="register"),
    path('login/', views.login_request, name='login'),
    path('frontpage/', core_views.frontpage, name='frontpage'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('my-store/', views.my_store, name='my_store'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-store/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]