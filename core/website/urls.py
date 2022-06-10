
from django.urls import path
from .views import *

app_name = 'website'
urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    path('', IndexView.as_view(), name='index'),
    path('product/<str:prod_id>/', ProductView.as_view(), name='product'),
    path('all-products/', AllProductsView.as_view(), name='all_products'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('review-product/<str:prod_id>/',
         ReviewProductView.as_view(), name='review_product'),

    path('newsletter/', SubscriptionView.as_view(), name='newsletter'),
]
