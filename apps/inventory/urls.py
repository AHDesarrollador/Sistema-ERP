from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Suppliers
    path('suppliers/', views.SupplierListCreateView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    
    # Products
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/low-stock/', views.LowStockProductsView.as_view(), name='low-stock-products'),
    
    # Stock Movements
    path('stock-movements/', views.StockMovementListCreateView.as_view(), name='stock-movement-list'),
    path('stock-movements/<int:pk>/', views.StockMovementDetailView.as_view(), name='stock-movement-detail'),
    
    # Stats
    path('stats/', views.InventoryStatsView.as_view(), name='inventory-stats'),
]