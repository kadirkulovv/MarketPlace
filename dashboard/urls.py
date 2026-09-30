from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.seller_dashboard_view, name='seller_dashboard'),
    path('products/', views.ProductListView.as_view(), name='seller_products'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/stock/', views.seller_update_stock_view, name='update_stock'),
    path('orders/', views.seller_orders_view, name='seller_orders'),
]
