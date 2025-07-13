from django.contrib import admin
from .models import Customer, Sale, SaleItem, SaleReport

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'email', 'phone']

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'customer', 'total_amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['sale_number', 'customer__name']
    readonly_fields = ['sale_number', 'user']
    inlines = [SaleItemInline]

@admin.register(SaleReport)
class SaleReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'start_date', 'end_date', 'total_sales', 'total_transactions', 'generated_by']
    list_filter = ['report_type', 'generated_at']
    readonly_fields = ['generated_by', 'generated_at']
