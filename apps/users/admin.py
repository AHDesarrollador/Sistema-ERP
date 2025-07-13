from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_manager', 'can_view_dashboard', 'is_staff']
    list_filter = ['is_manager', 'is_staff', 'is_superuser', 'department', 'can_view_dashboard', 'can_manage_inventory', 'can_manage_sales']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'department', 'is_manager')}),
        ('ERP Permissions', {'fields': ('can_view_dashboard', 'can_manage_inventory', 'can_manage_sales')}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'birth_date']
    list_filter = ['location']
