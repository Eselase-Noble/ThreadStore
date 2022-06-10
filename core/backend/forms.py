from django import forms

from .models import Banner, Merchant, Product, Category, Review, Subscription


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = [
            'prod_id',
            'extr_images',
            'category',
            'review',
            'image',
            'published',
            'views',
        ]


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["title", "image", "link", "published", "product_id"]


class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        exclude = [
            "live",
            "date_created",
            "approved",
            "date_modified",
            "created_by",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['product', 'rating', 'created_at']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email', ]
