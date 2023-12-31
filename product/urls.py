from .views import ProductsList, ProductDetail
from django.urls import path

app_name = 'product'

urlpatterns = [
    # path('products/all/', ProductsList.as_view(), name='all-products-list'),
    path('products/<path:category_path>/', ProductsList.as_view(), name='products-list'),
    path('product/<path:category_path>/<slug:slug>/', ProductDetail.as_view(), name='product-detail')
]
