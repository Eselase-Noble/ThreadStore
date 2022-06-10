
from django.urls import path
from .views import *

app_name = 'backend'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('create-product/', CreateProductView.as_view(), name='create_product'),
    path('update-product/<str:prod_id>/',
         UpdateProductView.as_view(), name='update_product'),
    path('products/', ListProductView.as_view(), name='products'),
    path('products/<str:prod_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('bulk-upload/', BulkProductUploadView.as_view(), name='bulk_upload'),
    path('delete-product/',
         DeleteProductView.as_view(), name='delete_product'),

    path('banner/', ListBannerView.as_view(), name='banners'),
    path('new-banner/', CreateBannerView.as_view(), name='new_banner'),

    path('users/', ListUserView.as_view(), name='users'),
    path('new-staff/', CreateStaffView.as_view(), name='new_staff'),

    path('new-category/', CreateCategoryView.as_view(), name='new_category'),
    path('categories/', ListCategoryView.as_view(), name='categories'),

    path('merchants/', ListMerchantView.as_view(), name='merchants'),
    path('new-merchant/', CreateMerchantView.as_view(), name='new_merchant'),

    path('extra-images/<int:pk>/',
         UploadExtraImagesView.as_view(), name='extra_images'),


    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('update-profile-picture/', UpdateProfilePicView.as_view(),
         name='update_profile_pic'),
    path('remove-profile-pic/', RemoveProfilePicView.as_view(),
         name='remove_profile_pic'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
