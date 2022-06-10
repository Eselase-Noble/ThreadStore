from contextlib import ContextDecorator
from unicodedata import category
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.utils.html import strip_tags
from django.contrib import messages

from backend.forms import ReviewForm, SubscriptionForm
from backend.models import Category, ExtraProductImage, Product, Review


class HomeView(View):
    template = 'website/home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)


class IndexView(View):
    template = 'website/index.html'

    def get(self, request, *args, **kwargs):
        latest_products = Product.objects.all().order_by('-created_at')[:5]
        top_choice_products = Product.objects.all().order_by(
            '-views')[:10]
        suggested_products = Product.objects.all().order_by('?')[:5]
        reviews = Review.objects.all().order_by('?')[:9]
        categories = Category.objects.all()
        context = {
            'latest_products': latest_products,
            'suggested_products': suggested_products,
            'top_choice_products': top_choice_products,
            'categories': categories,
            'reviews': reviews,
        }
        return render(request, self.template, context)


class ProductView(View):
    template = 'website/product.html'

    def get(self, request, prod_id, *args, **kwargs):
        product = Product.objects.filter(prod_id=prod_id).first()
        # increment views before proceeding to the page
        product.views += 1
        product.save()
        reviews = Review.objects.filter(product=product)
        categories = Category.objects.all()
        prod_cat = product.category if product else Category.objects.first()
        extra_images = ExtraProductImage.objects.filter(product=product)
        suggested_products = Product.objects.filter(
            category=prod_cat).exclude(prod_id=prod_id).order_by('?')[:5]
        context = {
            'product': product,
            'suggested_products': suggested_products,
            'categories': categories,
            'extra_images': extra_images,
            'reviews': reviews,
        }
        return render(request, self.template, context)


class AllProductsView(View):
    template = 'website/all_products.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, self.template, context)


class CategoryView(View):
    template = 'website/category.html'

    def get(self, request, pk, *args, **kwargs):
        categories = Category.objects.all()
        category = Category.objects.filter(id=pk).first()
        if not category:
            # fallback category
            category = Category.objects.first()
        products = Product.objects.filter(category=category, published=True)
        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, self.template, context)


class ReviewProductView(View):
    def get(self, request, prod_id, *args, **kwargs):
        return redirect('website:product', prod_id=prod_id)

    def post(self, request, prod_id, *args, **kwargs):
        form = ReviewForm(request.POST)
        product = Product.objects.filter(prod_id=prod_id).first()
        print(prod_id)
        print(product)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, 'Review submitted successfully!')
            print('Review submitted successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for field, error in form.errors.items():
                error = strip_tags(error)
                message = f"{field}: {error}"
                messages.error(request, message)
                print(message)
                return redirect(request.META.get("HTTP_REFERER"))


class SubscriptionView(View):
    def get(self, request, *args, **kwargs):
        return redirect('website:index')

    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'You have successfully subscribed to our news letter')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for field, error in form.errors.items():
                error = strip_tags(error)
                message = f"{field}: {error}"
                messages.error(request, message)
                return redirect(request.META.get("HTTP_REFERER"))
        return redirect('website:index')
