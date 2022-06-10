import random
import string
from django.db import models
from ckeditor.fields import RichTextField
from accounts.models import Account

from core.utils.constants import DEFAULT_IMAGE_URL


class Review(models.Model):
    """Review model"""
    user = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_being_reviewed', null=True, blank=True)
    title = models.CharField(max_length=100, default='I am satisfied')
    review = RichTextField(blank=True)
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name if self.product else 'No product'


class Category(models.Model):
    """Category of products model"""
    name = models.CharField(max_length=50)
    description = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_num_of_products(self):
        return Product.objects.filter(category=self, published=True).count()

    def __str__(self):
        return self.name if self.name else 'Category'


class ExtraProductImage(models.Model):
    '''To store extra images of a product: mostly 6 images per product'''
    image = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True, related_name='extra_images')

    def __str__(self):
        return self.image.url


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="uploads/images/banners/")
    link = models.URLField(null=True, blank=True, default="")
    published = models.BooleanField(default=False)
    product_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "banners"

    def get_image(self):
        return self.image.url if self.image else '/assets/img/card.jpg'

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    '''Database table to store products'''
    def generate_id():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    prod_id = models.CharField(
        max_length=10, primary_key=True, default=generate_id)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='images/', null=True, blank=True)  # main image
    image_url = models.URLField(
        default=DEFAULT_IMAGE_URL),
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ManyToManyField(Review, blank=True, related_name='reviews')
    description = RichTextField()
    key_features = RichTextField()
    views = models.IntegerField(default=0)

    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_rating(self):
        '''Returns average rating of a product'''
        reviews = Review.objects.filter(product=self)
        rating = 0
        for review in reviews:
            rating += review.rating
        if len(reviews) > 0:
            return rating / len(reviews)
        else:
            return 0

    def get_total_rating(self):
        '''Returns total number of reviews of a product'''
        return Review.objects.filter(product=self).count()

    def get_total_views(self):
        return ProductView.objects.filter(product=self).count()

    def get_image(self):
        '''
        Returns the image url of the product. 
        If no image is found, returns the default image url
        '''
        return self.image.url if self.image else 'assets/img/product-1.jpg'

    def get_extra_images(self):
        '''Returns the extra images of the product'''
        return ExtraProductImage.objects.filter(product=self)

    def __str__(self):
        return self.name


class DailyVisit(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True)
    visit_url = models.CharField(max_length=200, blank=True, null=True)
    date_of_visit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user if self.user else f'Anonymouse User {self.pk}'


class ProductView(models.Model):
    user = models.ForeignKey(Account, null=True, blank=True,
                             on_delete=models.CASCADE, related_name='viewer')
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.CASCADE)
    date_viewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name if self.product else f'Anonymous Product {self.pk}'


class Merchant(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=100)
    company_phone = models.CharField(max_length=100)
    company_email = models.EmailField(max_length=100)
    company_website = models.URLField(max_length=100)
    company_logo = models.ImageField(upload_to='merchant_logo')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Account,
                                   on_delete=models.CASCADE,
                                   related_name='created_by',
                                   null=True)
    approved = models.BooleanField(default=False)
    live = models.BooleanField(default=False)

    class Meta:
        db_table = "merchants"

    permissions = (("approve_merchant", "Can approve merchant"), )

    def get_image(self):
        return self.company_logo.url if self.company_logo else '/assets/img/logo.png'

    def __str__(self):
        return self.company_name


class Subscription(models.Model):
    '''Models to collect user emails from newsletter subscription'''
    email = models.EmailField()

    def __str__(self):
        return self.email
