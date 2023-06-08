from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.core.files import File

from io import BytesIO
from PIL import Image
from phone_field import PhoneField

from vendors.models import Vendor

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
    slug = models.SlugField(null=False, unique=True) ## null=False and unique=True, to automatically add slug on product creation
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self): ## function to automatically add slug on product creation
        return reverse('category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

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
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE, default=True)
    category = models.ForeignKey(Category, related_name= 'products', on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/',null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnail', blank=True, null=True)
    price = models.IntegerField()
    amount=models.IntegerField(default=0, blank=True, null=True)
    minamount=models.IntegerField(default=3, blank=True, null=True)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    detail=RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS, default=ACTIVE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def get_display_price(self): ### to display price in decimal of the product on the front page
        return self.price / 100

    class Meta: #this function sorts products in the order of newly created to be listed first on the front page
        ordering = ('-create_at',)

    def image_tag(self): ## method to create a fake table field in read only mode
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    def get_absolute_url(self): ## function to automatically add slug on product creation
        return reverse('category_detail', kwargs={'slug': self.slug})

    image_tag.short_description = 'Image'

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
    
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Images'
        verbose_name_plural = 'Images'

class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = PhoneField(blank=False, help_text='Contact phone number')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    
class OrderItem(models.Model):
    SHIPPED = 'shipped'
    DELETED = 'deleted'
    ACTIVE = 'active'
    DELIVERED = 'delivered'
    STATUS = (
        ('ACTIVE', 'Active'),
        ('SHIPPED', 'shipped'),
        ('DELIVERED', 'delivered'),
        ('DELETED', 'deleted'),
    )

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    status=models.CharField(max_length=10,choices=STATUS, default=ACTIVE)
    
    def get_display_price(self):
        return self.price
    
    def get_status(self):
        return self.status