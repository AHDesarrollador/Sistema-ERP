from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg, F
from django.db import models
from django.core.exceptions import PermissionDenied
from apps.inventory.models import Product, Category
from apps.sales.models import Sale
from datetime import datetime, timedelta

def check_dashboard_permission(user):
    """Check if user has dashboard access"""
    if user.is_superuser:
        return True
    return user.can_view_dashboard or user.has_perm('users.view_dashboard')

@login_required
def dashboard_view(request):
    """Main dashboard view - requires authentication and dashboard permission"""
    # Check if user has dashboard permission
    if not check_dashboard_permission(request.user):
        messages.error(request, 'You do not have permission to access the dashboard. Please contact your administrator.')
        return render(request, 'dashboard/access_denied.html', {
            'user': request.user,
            'required_permission': 'Dashboard Access'
        })
    
    # Get user permissions for frontend
    user_permissions = {
        'can_view_dashboard': check_dashboard_permission(request.user),
        'can_manage_inventory': request.user.is_superuser or request.user.can_manage_inventory,
        'can_manage_sales': request.user.is_superuser or request.user.can_manage_sales,
        'is_admin': request.user.is_superuser,
        'is_manager': request.user.is_manager,
    }
    
    return render(request, 'dashboard/dashboard.html', {
        'user_permissions': user_permissions,
        'user': request.user
    })

def dashboard_api_data(request):
    """API endpoint for dashboard data"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Check dashboard permission
    if not check_dashboard_permission(request.user):
        return JsonResponse({'error': 'Dashboard access denied'}, status=403)
    
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
