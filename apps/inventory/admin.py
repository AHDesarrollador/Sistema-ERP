from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_person', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'current_stock', 'minimum_stock', 'selling_price', 'is_low_stock']
    list_filter = ['category', 'supplier', 'is_active']
    search_fields = ['name', 'sku', 'barcode']
    readonly_fields = ['is_low_stock']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'user', 'created_at']
    list_filter = ['movement_type', 'created_at']
    readonly_fields = ['user', 'created_at']
