from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse
from django.utils.safestring import mark_safe

# the category model is for adding category fields for the products by the admin or the vendor
class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    DELETED = 'deleted'
    ACTIVE = 'active'
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
        ('DELETED', 'deleted'),
        ('DRAFT', 'draft'),
        ('ACTIVE', 'Active'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    user = models.ForeignKey(User, related_name= 'products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name= 'products', on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/',null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0, blank=True, null=True)
    minamount=models.IntegerField(default=3, blank=True, null=True)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    detail=RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(max_length=50)
    status=models.CharField(max_length=10,choices=STATUS, default=ACTIVE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price

    class Meta: #this function sorts products in the order of newly created to be listed first on the front page
        ordering = ('-create_at',)

     ## method to create a fake table field in read only mode
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Images'
        verbose_name_plural = 'Images'
    