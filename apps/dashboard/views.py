from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg, F
from django.db import models
from apps.inventory.models import Product, Category
from apps.sales.models import Sale
from datetime import datetime, timedelta

def dashboard_view(request):
    """Main dashboard view"""
    return render(request, 'dashboard/dashboard.html')

def dashboard_api_data(request):
    """API endpoint for dashboard data"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Get date ranges
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Inventory stats
    inventory_data = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'low_stock_products': Product.objects.filter(
            current_stock__lte=F('minimum_stock'),
            is_active=True
        ).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_stock_value': Product.objects.filter(is_active=True).aggregate(
            total=Sum(F('current_stock') * F('cost_price'))
        )['total'] or 0
    }
    
    # Sales stats
    sales_data = {
        'today_sales': Sale.objects.filter(
            created_at__date=today,
            status='COMPLETED'
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        
        'week_sales': Sale.objects.filter(
            created_at__date__gte=week_ago,
            status='COMPLETED'
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        
        'month_sales': Sale.objects.filter(
            created_at__date__gte=month_ago,
            status='COMPLETED'
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        
        'total_transactions': Sale.objects.filter(status='COMPLETED').count()
    }
    
    return JsonResponse({
        'inventory': inventory_data,
        'sales': sales_data
    })
