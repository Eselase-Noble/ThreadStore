import csv
import io
from django.contrib.auth import update_session_auth_hash
from django.utils.html import strip_tags
from accounts.models import Account
from core.utils.constants import StatusCodes as S
from django.contrib import messages
from .forms import BannerForm, CategoryForm, MerchantForm, ProductForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View

from .models import Banner, Category, Merchant, Product, ExtraProductImage, Review


class DashboardView(View):
    template = 'backend/dashboard.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)


class CreateCategoryView(View):
    template = 'backend/forms/create_update_category.html'

    def get(self, request, *args, **kwargs):
        context = {'head': 'Create'}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully")
            return redirect('backend:categories')
        else:
            messages.error(request, "Category created successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ListCategoryView(View):
    template = 'backend/categories.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('-id')
        context = {'categories': categories}
        return render(request, self.template, context)


class CreateProductView(View):
    template = 'backend/forms/create_update_product.html'
    template_2 = 'backend/forms/upload_extra_images.html'

    def get(self, request,  *args, **kwargs):
        categories = Category.objects.all().order_by('-id')
        context = {'head': 'Create', 'categories': categories}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES or None)
        pk = request.POST.get('category')
        # category = Category.objects.filter(
        #     id=pk).first()
        category = Category.objects.filter(
            id=request.POST.get('category')).first()
        published = True if request.POST.get(
            'published') == S.PUBLISHED.value else False
        if form.is_valid():
            form.save(commit=False)
            # if category:
            #     form.category = category
            form.category = category
            form.published = published
            form.save()
            messages.success(request, "Product Successfully")
            return render(request, self.template_2, {'product': form})
        else:
            for field, error in form.errors.items():
                error = strip_tags(error)
                message = f"{field}: {error}"
                messages.error(request, message)
                return redirect(request.META.get("HTTP_REFERER"))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UploadExtraImagesView(View):
    template = 'backend/forms/upload_extra_images.html'

    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.filter(id=pk).first()
        context = {'product': product}
        return render(request, self.template, context)

    def post(self, request, pk, *args, **kwargs):
        images = request.FILES.getlist('images')
        product = Product.objects.filter(id=pk).first()
        if images:
            for image in images:
                ExtraProductImage.objects.create(image=image, product=product)
        messages.success(request, 'Images uploaded successfully')
        return redirect('backend:products')


class ListProductView(View):
    template = 'backend/products.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-created_at')
        context = {
            'products': products
        }
        return render(request, self.template, context)


class UserProfileView(View):
    template = 'backend/user_profile.html'

    def get(self, request,  *args, **kwargs):
        context = {'user': request.user}
        return render(request, self.template, context)


class UpdateProductView(View):
    template_name = 'backend/forms/create_update_product.html'

    # @method_decorator(MustLogin)
    def get(self, request, prod_id, *args, **kwargs):
        product = Product.objects.filter(prod_id=prod_id).first()
        categories = Category.objects.all()
        context = {
            'product': product,
            'head': 'Update',
            'categories': categories,
        }
        return render(request, self.template_name, context)

    # @method_decorator(MustLogin)
    def post(self, request, prod_id, *args, **kwargs):
        image = request.FILES.get('image')
        form = ProductForm(
            request.POST, instance=Product.objects.get(prod_id=prod_id))
        published = True if request.POST.get(
            'published') == S.PUBLISHED.value else False
        category = Category.objects.filter(
            id=request.POST.get('category')).first()
        if form.is_valid():
            product = form.save()
            if image:
                product.image.delete()
                product.image = image

            product.published = published
            product.category = category
            product.save()
            messages.success(request, 'Product Updated Successfully')
            return redirect('backend:products')
        else:
            # Display first error in the form
            for field, error in form.errors.items():
                error = strip_tags(error)
                message = f"{field}: {error}"
                messages.error(request, message)
                return redirect(request.META.get("HTTP_REFERER"))
            return redirect('backend:products')


class ProductDetailView(View):
    template = 'backend/product_detail.html'

    def get(self, request, prod_id, *args, **kwargs):
        product = Product.objects.filter(prod_id=prod_id).first()

        reviews = Review.objects.filter(product=product)
        context = {'product': product}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(
            prod_id=request.POST.get('prod_id')).first()
        published = True if request.POST.get(
            'published') == S.PUBLISHED.value else False
        product.published = published
        product.save()
        if published:
            messages.success(request, 'Product Published Successfully')
        else:
            messages.success(request, 'Product Unpublished Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ListUserView(View):
    template = 'backend/users.html'

    def get(self, request, *args, **kwargs):
        users = Account.objects.all().order_by('-id')
        context = {'users': users}
        return render(request, self.template, context)


class CreateStaffView(View):
    template = 'backend/forms/create_update_staff.html'

    def get(self, request, *args, **kwargs):
        context = {'head': 'Create'}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        Account.objects.create_superuser(
            email=request.POST.get('email'), password=request.POST.get('password'),
            phone=request.POST.get('phone'), name=request.POST.get('name')
        )
        messages.success(request, 'Staff Member Account Created successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ListMerchantView(View):
    template = 'backend/merchants.html'

    def get(self, request, *args, **kwargs):
        merchants = Merchant.objects.all().order_by('-id')
        context = {'merchants': merchants}
        return render(request, self.template, context)


class CreateMerchantView(View):
    template = 'backend/forms/create_update_merchant.html'

    def get(self, request, *args, **kwargs):
        context = {'head': 'Create'}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        form = MerchantForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.created_by = request.user
            form.save()
            messages.success(request, 'Merchant Created Successfully')
            return redirect('backend:merchants')
        else:
            # Display first error in the form
            for field, error in form.errors.items():
                error = strip_tags(error)
                message = f"{field}: {error}"
                messages.error(request, message)
            return redirect('backend:merchants')


class ListBannerView(View):
    template = 'backend/banners.html'

    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by('-id')
        context = {'banners': banners}
        return render(request, self.template, context)


class CreateBannerView(View):
    template = 'backend/forms/create_update_banner.html'

    def get(self, request, *args, **kwargs):
        context = {'head': 'Create'}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        form = BannerForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner Created Successfully!')
            return redirect('backend:banners')
        else:
            for field, error in form.errors.items():
                error = strip_tags(error)
                message = f"{field}: {error}"
                messages.error(request, message)
            return HttpResponseRedirect(request.META.get('HTTP_REFERRER'))


class UpdateProfileView(View):
    # @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:profile')

    # @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        user = request.user
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.name = request.POST.get('name')
        user.country = request.POST.get('country')
        user.about = request.POST.get('about')
        user.email = request.POST.get('email')
        user.twitter = request.POST.get('twitter')
        user.facebook = request.POST.get('facebook')
        user.instagram = request.POST.get('instagram')
        user.linkedIn = request.POST.get('linkedin')
        user.save()
        messages.success(request, 'Profile updated successfully')
        print("Profile updated successfully")
        return redirect('backend:profile')


class UpdateProfilePicView(View):
    # @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:profile')

    # @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        user = request.user
        photo = request.FILES.get('photo')
        if photo:
            user.photo = photo
            user.save()
            messages.success(request, 'Profile picture updated successfully')
            print("Profile picture updated successfully")
            return redirect('backend:profile')
        else:
            messages.error(request, 'No Picture Selected!')
            print('Profile picture not updated!')
            return redirect('backend:profile')


class RemoveProfilePicView(View):
    def get(self, request, *args, **kwargs):
        return redirect('backend:profile')

    def post(self, request, *args, **kwargs):
        user = request.user
        user.photo = None
        user.save()
        messages.success(request, 'Profile Picture Removed Successfully')
        return redirect('backend:profile')


class ChangePasswordView(View):
    # @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:profile')

    # @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if request.user.check_password(current_password):
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')
                return redirect('backend:profile')
            else:
                messages.error(
                    request,
                    'New password and confirm password does not match')
                print('New password and confirm password does not match')
                return redirect('backend:profile')
        else:
            messages.error(request, 'Old Password Not Valid!')
            print('Old Password Not Valid!')
            return redirect('backend:profile')


class BulkProductUploadView(View):
    template = 'backend/forms/bulk_product_upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('csv_file')
        dataset = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(dataset)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Product.objects.update_or_create(
                prod_id=column[0],
                name=column[1],
                price=column[2],
                image_url=column[3],
                brand=column[4],
                category=column[5],
                description=column[6],
                key_features=column[7],
            )
        messages.success(request, "Products Uploaded Successfully")
        return redirect('products')


class DeleteProductView(View):
    # @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return redirect('backend:products')

    # @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = Product.objects.filter(prod_id=product_id).first()
        product.delete()
        messages.success(request, 'Product deleted successfully')
        print("Product deleted successfully")
        return redirect('backend:products')
