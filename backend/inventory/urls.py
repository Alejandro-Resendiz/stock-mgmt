from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<uuid:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('stores/', views.StoreListAPIView.as_view(), name='store-list'),
    path('stores/<uuid:store_id>/inventory/', views.store_inventory, name='store-inventory'),
    path('inventory/transfer/', views.transfer_stock, name='transfer-stock'),
    path('inventory/alerts/', views.inventory_alerts, name='inventory-alerts'),
]