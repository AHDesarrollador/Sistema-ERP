"""
Custom permissions for ERP Dashboard system
"""
from rest_framework import permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class DashboardViewPermission(permissions.BasePermission):
    """
    Custom permission for dashboard access
    """
    message = "You don't have permission to access the dashboard."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusers always have access
        if request.user.is_superuser:
            return True
        
        # Check if user has dashboard view permission
        return request.user.has_perm('users.view_dashboard')

class InventoryManagerPermission(permissions.BasePermission):
    """
    Permission for inventory management
    """
    message = "You don't have permission to manage inventory."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Check if user is manager or has inventory permissions
        return (request.user.is_manager or 
                request.user.has_perm('inventory.view_product') or
                request.user.has_perm('inventory.change_product'))

class SalesManagerPermission(permissions.BasePermission):
    """
    Permission for sales management
    """
    message = "You don't have permission to manage sales."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return (request.user.is_manager or
                request.user.has_perm('sales.view_sale') or
                request.user.has_perm('sales.change_sale'))

def create_dashboard_permission():
    """
    Create custom dashboard permission
    """
    try:
        content_type = ContentType.objects.get_for_model(
            apps.get_model('users', 'User')
        )
        
        permission, created = Permission.objects.get_or_create(
            codename='view_dashboard',
            name='Can view dashboard',
            content_type=content_type,
        )
        
        return permission
    except Exception as e:
        print(f"Error creating dashboard permission: {e}")
        return None