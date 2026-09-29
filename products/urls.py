from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<slug:slug>/', views.category_products_view, name='category_products'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
]
