from django.contrib import admin

from .models import Category, Product, Images

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status','image']
    list_filter = ['category']
    inlines = [ProductImageInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
